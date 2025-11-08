"""
Dynamic Tool Generator
Allows creating tools on-the-fly from templates or custom configurations
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import uuid
import yaml
from pathlib import Path
from enum import Enum


class ToolTemplate(str, Enum):
    """Predefined tool templates"""
    DUCKDUCKGO_SEARCH = "duckduckgo_search"
    API_REST = "api_rest"
    API_GRAPHQL = "api_graphql"
    WEB_SCRAPER = "web_scraper"
    DATABASE_SQL = "database_sql"
    FILE_READER = "file_reader"
    FILE_WRITER = "file_writer"
    PYTHON_EXECUTOR = "python_executor"
    SHELL_COMMAND = "shell_command"
    HTTP_REQUEST = "http_request"
    CUSTOM = "custom"


class DynamicToolGenerator:
    """Generate tools dynamically from templates or specifications"""
    
    def __init__(self, config_dir: str = "config/tools"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined tool templates"""
        return {
            ToolTemplate.DUCKDUCKGO_SEARCH: {
                "type": "websearch",
                "config": {
                    "engine": "duckduckgo",
                    "max_results": 5,
                    "region": "wt-wt",
                    "safesearch": "moderate",
                    "timelimit": None
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "max_results": {"type": "integer", "default": 5},
                        "region": {"type": "string", "default": "wt-wt"}
                    },
                    "required": ["query"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "results": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "url": {"type": "string"},
                                    "snippet": {"type": "string"}
                                }
                            }
                        },
                        "query": {"type": "string"},
                        "count": {"type": "integer"}
                    }
                }
            },
            
            ToolTemplate.API_REST: {
                "type": "api",
                "config": {
                    "method": "GET",
                    "headers": {},
                    "timeout": 10.0
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "API endpoint URL"},
                        "method": {"type": "string", "enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
                        "params": {"type": "object"},
                        "body": {"type": "object"},
                        "headers": {"type": "object"}
                    },
                    "required": ["url"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "status_code": {"type": "integer"},
                        "body": {"type": "string"},
                        "json": {"type": "object"},
                        "headers": {"type": "object"}
                    }
                }
            },
            
            ToolTemplate.API_GRAPHQL: {
                "type": "graphql",
                "config": {
                    "timeout": 10.0,
                    "headers": {"Content-Type": "application/json"}
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "GraphQL endpoint"},
                        "query": {"type": "string", "description": "GraphQL query"},
                        "variables": {"type": "object"}
                    },
                    "required": ["url", "query"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "data": {"type": "object"},
                        "errors": {"type": "array"}
                    }
                }
            },
            
            ToolTemplate.WEB_SCRAPER: {
                "type": "http",
                "config": {
                    "method": "GET",
                    "parser": "html",
                    "selectors": {}
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string"},
                        "selectors": {"type": "object", "description": "CSS selectors to extract"}
                    },
                    "required": ["url"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "extracted_data": {"type": "object"},
                        "raw_html": {"type": "string"}
                    }
                }
            },
            
            ToolTemplate.DATABASE_SQL: {
                "type": "database",
                "config": {
                    "db_type": "sql",
                    "connection_string": "",
                    "safe_mode": True
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "params": {"type": "array"}
                    },
                    "required": ["query"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "rows": {"type": "array"},
                        "row_count": {"type": "integer"}
                    }
                }
            },
            
            ToolTemplate.FILE_READER: {
                "type": "file",
                "config": {
                    "operation": "read",
                    "encoding": "utf-8",
                    "safe_path_check": True
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "encoding": {"type": "string", "default": "utf-8"}
                    },
                    "required": ["path"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "path": {"type": "string"},
                        "size": {"type": "integer"}
                    }
                }
            },
            
            ToolTemplate.FILE_WRITER: {
                "type": "file",
                "config": {
                    "operation": "write",
                    "encoding": "utf-8",
                    "create_dirs": True
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"},
                        "mode": {"type": "string", "enum": ["write", "append"], "default": "write"}
                    },
                    "required": ["path", "content"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "path": {"type": "string"},
                        "bytes_written": {"type": "integer"}
                    }
                }
            },
            
            ToolTemplate.PYTHON_EXECUTOR: {
                "type": "python",
                "config": {
                    "sandbox": True,
                    "timeout": 30,
                    "allowed_imports": []
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "code": {"type": "string"},
                        "timeout": {"type": "number", "default": 30}
                    },
                    "required": ["code"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "output": {"type": "string"},
                        "error": {"type": "string"},
                        "execution_time": {"type": "number"}
                    }
                }
            },
            
            ToolTemplate.SHELL_COMMAND: {
                "type": "shell",
                "config": {
                    "shell": "bash",
                    "timeout": 60,
                    "safe_mode": True
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string"},
                        "cwd": {"type": "string"},
                        "env": {"type": "object"}
                    },
                    "required": ["command"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "stdout": {"type": "string"},
                        "stderr": {"type": "string"},
                        "exit_code": {"type": "integer"}
                    }
                }
            },
            
            ToolTemplate.HTTP_REQUEST: {
                "type": "http",
                "config": {
                    "method": "GET",
                    "timeout": 10.0,
                    "follow_redirects": True
                },
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string"},
                        "method": {"type": "string"},
                        "headers": {"type": "object"},
                        "params": {"type": "object"},
                        "body": {"type": ["object", "string"]}
                    },
                    "required": ["url"]
                },
                "output_schema": {
                    "type": "object",
                    "properties": {
                        "status_code": {"type": "integer"},
                        "headers": {"type": "object"},
                        "body": {"type": "string"},
                        "json": {"type": ["object", "array", "null"]}
                    }
                }
            },
            
            ToolTemplate.CUSTOM: {
                "type": "custom",
                "config": {},
                "input_schema": {
                    "type": "object",
                    "properties": {}
                },
                "output_schema": {
                    "type": "object",
                    "properties": {}
                }
            }
        }
    
    def create_tool_from_template(
        self,
        template: ToolTemplate,
        name: str,
        description: Optional[str] = None,
        config_overrides: Optional[Dict[str, Any]] = None,
        save_to_disk: bool = True
    ) -> Dict[str, Any]:
        """Create a tool from a predefined template"""
        
        # Get template
        template_def = self.templates.get(template)
        if not template_def:
            raise ValueError(f"Unknown template: {template}")
        
        # Generate unique ID
        tool_id = f"{template.value}_{uuid.uuid4().hex[:8]}"
        
        # Merge config
        config = template_def["config"].copy()
        if config_overrides:
            config.update(config_overrides)
        
        # Create tool definition
        tool_def = {
            "id": tool_id,
            "name": name,
            "description": description or f"Tool created from {template.value} template",
            "type": template_def["type"],
            "config": config,
            "input_schema": template_def["input_schema"],
            "output_schema": template_def["output_schema"],
            "version": "v1",
            "created_at": datetime.now().isoformat(),
            "template": template.value
        }
        
        # Save to disk if requested
        if save_to_disk:
            self._save_tool_to_yaml(tool_def)
        
        return tool_def
    
    def create_custom_tool(
        self,
        name: str,
        tool_type: str,
        config: Dict[str, Any],
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        save_to_disk: bool = True
    ) -> Dict[str, Any]:
        """Create a completely custom tool"""
        
        tool_id = f"custom_{uuid.uuid4().hex[:8]}"
        
        tool_def = {
            "id": tool_id,
            "name": name,
            "description": description or f"Custom {tool_type} tool",
            "type": tool_type,
            "config": config,
            "input_schema": input_schema or {
                "type": "object",
                "properties": {}
            },
            "output_schema": output_schema or {
                "type": "object",
                "properties": {}
            },
            "version": "v1",
            "created_at": datetime.now().isoformat(),
            "template": "custom"
        }
        
        if save_to_disk:
            self._save_tool_to_yaml(tool_def)
        
        return tool_def
    
    def create_duckduckgo_search_tool(
        self,
        name: str = "DuckDuckGo Search",
        max_results: int = 5,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Quick helper to create a DuckDuckGo search tool"""
        
        return self.create_tool_from_template(
            template=ToolTemplate.DUCKDUCKGO_SEARCH,
            name=name,
            description=description or "DuckDuckGo web search tool",
            config_overrides={
                "max_results": max_results,
                "region": region,
                "safesearch": safesearch,
                "timelimit": timelimit
            }
        )
    
    def create_api_tool(
        self,
        name: str,
        base_url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Quick helper to create an API tool"""
        
        return self.create_tool_from_template(
            template=ToolTemplate.API_REST,
            name=name,
            description=description or f"REST API tool for {base_url}",
            config_overrides={
                "url": base_url,
                "method": method,
                "headers": headers or {}
            }
        )
    
    def create_tool_from_spec(
        self,
        spec: Dict[str, Any],
        save_to_disk: bool = True
    ) -> Dict[str, Any]:
        """Create a tool from a complete specification dictionary"""
        
        # Ensure required fields
        if "id" not in spec:
            spec["id"] = f"tool_{uuid.uuid4().hex[:8]}"
        
        if "created_at" not in spec:
            spec["created_at"] = datetime.now().isoformat()
        
        if "version" not in spec:
            spec["version"] = "v1"
        
        # Validate required fields
        required = ["name", "type", "config"]
        missing = [f for f in required if f not in spec]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        
        if save_to_disk:
            self._save_tool_to_yaml(spec)
        
        return spec
    
    def batch_create_tools(
        self,
        tool_specs: List[Dict[str, Any]],
        save_to_disk: bool = True
    ) -> List[Dict[str, Any]]:
        """Create multiple tools at once"""
        
        tools = []
        for spec in tool_specs:
            if "template" in spec:
                # Create from template
                template = ToolTemplate(spec["template"])
                tool = self.create_tool_from_template(
                    template=template,
                    name=spec["name"],
                    description=spec.get("description"),
                    config_overrides=spec.get("config", {}),
                    save_to_disk=save_to_disk
                )
            else:
                # Create custom
                tool = self.create_tool_from_spec(spec, save_to_disk=save_to_disk)
            
            tools.append(tool)
        
        return tools
    
    def _save_tool_to_yaml(self, tool_def: Dict[str, Any]) -> Path:
        """Save tool definition to YAML file"""
        
        file_path = self.config_dir / f"{tool_def['id']}.yaml"
        
        # Create clean dict for YAML (remove None values)
        clean_def = {k: v for k, v in tool_def.items() if v is not None}
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(clean_def, f, default_flow_style=False, sort_keys=False)
        
        return file_path
    
    def load_tool_from_yaml(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Load a tool definition from YAML file"""
        
        file_path = self.config_dir / f"{tool_id}.yaml"
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def list_available_templates(self) -> List[Dict[str, Any]]:
        """List all available tool templates"""
        
        return [
            {
                "template": template.value,
                "type": definition["type"],
                "description": f"Template for {template.value.replace('_', ' ')} tools"
            }
            for template, definition in self.templates.items()
        ]
    
    def get_template_schema(self, template: ToolTemplate) -> Dict[str, Any]:
        """Get the schema for a specific template"""
        
        template_def = self.templates.get(template)
        if not template_def:
            raise ValueError(f"Unknown template: {template}")
        
        return {
            "template": template.value,
            "type": template_def["type"],
            "config": template_def["config"],
            "input_schema": template_def["input_schema"],
            "output_schema": template_def["output_schema"]
        }


# Example usage and predefined tool recipes
class ToolRecipes:
    """Collection of common tool recipes"""
    
    @staticmethod
    def web_search_suite() -> List[Dict[str, Any]]:
        """Create a suite of web search tools"""
        return [
            {
                "template": "duckduckgo_search",
                "name": "Quick Web Search",
                "description": "Fast web search with 3 results",
                "config": {"max_results": 3}
            },
            {
                "template": "duckduckgo_search",
                "name": "Deep Web Search",
                "description": "Comprehensive search with 10 results",
                "config": {"max_results": 10}
            },
            {
                "template": "duckduckgo_search",
                "name": "News Search",
                "description": "Recent news (last day)",
                "config": {"max_results": 5, "timelimit": "d"}
            }
        ]
    
    @staticmethod
    def api_tools_suite() -> List[Dict[str, Any]]:
        """Create common API tools"""
        return [
            {
                "template": "api_rest",
                "name": "GitHub API",
                "description": "GitHub REST API",
                "config": {
                    "url": "https://api.github.com",
                    "headers": {"Accept": "application/vnd.github.v3+json"}
                }
            },
            {
                "template": "api_rest",
                "name": "JSONPlaceholder Test API",
                "description": "Testing and prototyping API",
                "config": {"url": "https://jsonplaceholder.typicode.com"}
            }
        ]
    
    @staticmethod
    def file_operations_suite() -> List[Dict[str, Any]]:
        """Create file operation tools"""
        return [
            {
                "template": "file_reader",
                "name": "Text File Reader",
                "description": "Read text files"
            },
            {
                "template": "file_writer",
                "name": "Text File Writer",
                "description": "Write text files"
            }
        ]


# Global generator instance
dynamic_tool_generator = DynamicToolGenerator()
