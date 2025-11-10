from fastapi import APIRouter, HTTPException, Body
from app.models import ToolDef
from app.storage import save, load, list_all, delete
from app.services.dynamic_tool_generator import dynamic_tool_generator, ToolTemplate, ToolRecipes
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

router = APIRouter()


# ============= Request Models =============

class DynamicToolFromTemplateRequest(BaseModel):
    """Request to create a tool from a template"""
    template: str
    name: str
    description: Optional[str] = None
    config_overrides: Optional[Dict[str, Any]] = None
    save_to_disk: bool = True


class DynamicToolCustomRequest(BaseModel):
    """Request to create a custom tool"""
    name: str
    type: str
    config: Dict[str, Any]
    input_schema: Optional[Dict[str, Any]] = None
    output_schema: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    save_to_disk: bool = True


class DuckDuckGoSearchToolRequest(BaseModel):
    """Quick create DuckDuckGo search tool"""
    name: str = "DuckDuckGo Search"
    max_results: int = 5
    region: str = "wt-wt"
    safesearch: str = "moderate"
    timelimit: Optional[str] = None
    description: Optional[str] = None


class BatchToolCreateRequest(BaseModel):
    """Create multiple tools at once"""
    tools: List[Dict[str, Any]]
    save_to_disk: bool = True


# ============= Original Endpoints =============

@router.post("/", response_model=ToolDef)
async def create_tool(tool: ToolDef):
    """Create a tool from a complete ToolDef"""
    # Generate ID if not provided or empty
    if not tool.id or tool.id.strip() == "":
        import uuid
        tool.id = f"tool_{uuid.uuid4().hex[:8]}"
    
    # Check if tool already exists
    existing = load("tools", tool.id)
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Tool with ID '{tool.id}' already exists. Use PUT to update or choose a different ID."
        )
    
    save("tools", tool.id, tool.model_dump())
    return tool


@router.get("/{tool_id}", response_model=ToolDef)
async def get_tool(tool_id: str):
    """Get a specific tool by ID"""
    data = load("tools", tool_id)
    if not data:
        raise HTTPException(status_code=404, detail="Tool not found")
    return data


@router.get("/", response_model=List[ToolDef])
async def list_tools():
    """List all available tools"""
    return list_all("tools")


@router.put("/{tool_id}", response_model=ToolDef)
async def update_tool(tool_id: str, tool: ToolDef):
    """Update an existing tool"""
    save("tools", tool_id, tool.model_dump())
    return tool


@router.delete("/{tool_id}")
async def delete_tool(tool_id: str):
    """Delete a tool"""
    ok = delete("tools", tool_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tool not found")
    return {"deleted": True}


# ============= Dynamic Tool Creation Endpoints =============

@router.get("/dynamic/templates")
async def list_templates():
    """List all available tool templates"""
    return {
        "templates": dynamic_tool_generator.list_available_templates()
    }


@router.get("/dynamic/templates/{template_name}")
async def get_template_schema(template_name: str):
    """Get the schema for a specific template"""
    try:
        template = ToolTemplate(template_name)
        return dynamic_tool_generator.get_template_schema(template)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/dynamic/from-template")
async def create_tool_from_template(request: DynamicToolFromTemplateRequest):
    """Create a tool dynamically from a template"""
    try:
        template = ToolTemplate(request.template)
        tool_def = dynamic_tool_generator.create_tool_from_template(
            template=template,
            name=request.name,
            description=request.description,
            config_overrides=request.config_overrides,
            save_to_disk=request.save_to_disk
        )
        
        # Also save to storage system
        if request.save_to_disk:
            save("tools", tool_def["id"], tool_def)
        
        return {
            "success": True,
            "tool": tool_def,
            "message": f"Tool '{request.name}' created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tool: {str(e)}")


@router.post("/dynamic/custom")
async def create_custom_tool(request: DynamicToolCustomRequest):
    """Create a completely custom tool"""
    try:
        tool_def = dynamic_tool_generator.create_custom_tool(
            name=request.name,
            tool_type=request.type,
            config=request.config,
            input_schema=request.input_schema,
            output_schema=request.output_schema,
            description=request.description,
            save_to_disk=request.save_to_disk
        )
        
        # Also save to storage system
        if request.save_to_disk:
            save("tools", tool_def["id"], tool_def)
        
        return {
            "success": True,
            "tool": tool_def,
            "message": f"Custom tool '{request.name}' created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create custom tool: {str(e)}")


@router.post("/dynamic/duckduckgo")
async def create_duckduckgo_tool(request: DuckDuckGoSearchToolRequest):
    """Quick endpoint to create a DuckDuckGo search tool"""
    try:
        tool_def = dynamic_tool_generator.create_duckduckgo_search_tool(
            name=request.name,
            max_results=request.max_results,
            region=request.region,
            safesearch=request.safesearch,
            timelimit=request.timelimit,
            description=request.description
        )
        
        # Save to storage system
        save("tools", tool_def["id"], tool_def)
        
        return {
            "success": True,
            "tool": tool_def,
            "message": f"DuckDuckGo search tool '{request.name}' created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create DuckDuckGo tool: {str(e)}")


@router.post("/dynamic/batch")
async def batch_create_tools(request: BatchToolCreateRequest):
    """Create multiple tools at once"""
    try:
        tools = dynamic_tool_generator.batch_create_tools(
            tool_specs=request.tools,
            save_to_disk=request.save_to_disk
        )
        
        # Save to storage system
        if request.save_to_disk:
            for tool in tools:
                save("tools", tool["id"], tool)
        
        return {
            "success": True,
            "tools": tools,
            "count": len(tools),
            "message": f"Successfully created {len(tools)} tools"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to batch create tools: {str(e)}")


@router.post("/dynamic/recipes/{recipe_name}")
async def create_from_recipe(recipe_name: str):
    """Create a predefined suite of tools from a recipe"""
    recipes = {
        "web_search": ToolRecipes.web_search_suite,
        "api_tools": ToolRecipes.api_tools_suite,
        "file_operations": ToolRecipes.file_operations_suite
    }
    
    if recipe_name not in recipes:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe '{recipe_name}' not found. Available: {list(recipes.keys())}"
        )
    
    try:
        tool_specs = recipes[recipe_name]()
        tools = dynamic_tool_generator.batch_create_tools(tool_specs, save_to_disk=True)
        
        # Save to storage system
        for tool in tools:
            save("tools", tool["id"], tool)
        
        return {
            "success": True,
            "recipe": recipe_name,
            "tools": tools,
            "count": len(tools),
            "message": f"Successfully created {len(tools)} tools from '{recipe_name}' recipe"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create tools from recipe: {str(e)}")


@router.get("/dynamic/recipes")
async def list_recipes():
    """List all available tool recipes"""
    return {
        "recipes": [
            {
                "name": "web_search",
                "description": "Suite of DuckDuckGo search tools (quick, deep, news)",
                "tool_count": 3
            },
            {
                "name": "api_tools",
                "description": "Common API tools (GitHub, JSONPlaceholder)",
                "tool_count": 2
            },
            {
                "name": "file_operations",
                "description": "File reader and writer tools",
                "tool_count": 2
            }
        ]
    }
