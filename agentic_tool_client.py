"""
AgenticApp Dynamic Tool Client
Easy-to-use Python client for creating and managing dynamic tools
"""

import requests
from typing import Dict, Any, List, Optional, Union
from enum import Enum


class ToolTemplate(str, Enum):
    """Available tool templates"""
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


class AgenticToolClient:
    """Client for creating and managing dynamic tools"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the client
        
        Args:
            base_url: Base URL of the AgenticApp backend
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    # ============= Template Methods =============
    
    def list_templates(self) -> List[Dict[str, Any]]:
        """
        List all available tool templates
        
        Returns:
            List of template information
        """
        response = self.session.get(f"{self.base_url}/tools/dynamic/templates")
        response.raise_for_status()
        return response.json()["templates"]
    
    def get_template_schema(self, template: Union[str, ToolTemplate]) -> Dict[str, Any]:
        """
        Get the schema for a specific template
        
        Args:
            template: Template name or enum
            
        Returns:
            Template schema
        """
        template_name = template.value if isinstance(template, ToolTemplate) else template
        response = self.session.get(f"{self.base_url}/tools/dynamic/templates/{template_name}")
        response.raise_for_status()
        return response.json()
    
    # ============= Tool Creation Methods =============
    
    def create_from_template(
        self,
        template: Union[str, ToolTemplate],
        name: str,
        description: Optional[str] = None,
        config_overrides: Optional[Dict[str, Any]] = None,
        save_to_disk: bool = True
    ) -> Dict[str, Any]:
        """
        Create a tool from a template
        
        Args:
            template: Template to use
            name: Tool name
            description: Tool description
            config_overrides: Config values to override
            save_to_disk: Whether to save to disk
            
        Returns:
            Created tool definition
        """
        template_name = template.value if isinstance(template, ToolTemplate) else template
        
        payload = {
            "template": template_name,
            "name": name,
            "description": description,
            "config_overrides": config_overrides or {},
            "save_to_disk": save_to_disk
        }
        
        response = self.session.post(
            f"{self.base_url}/tools/dynamic/from-template",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def create_duckduckgo_search(
        self,
        name: str = "DuckDuckGo Search",
        max_results: int = 5,
        region: str = "wt-wt",
        safesearch: str = "moderate",
        timelimit: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Quick method to create a DuckDuckGo search tool
        
        Args:
            name: Tool name
            max_results: Maximum number of results
            region: Search region
            safesearch: Safety level ("strict", "moderate", "off")
            timelimit: Time limit ("d", "w", "m", or None)
            description: Tool description
            
        Returns:
            Created tool definition
        """
        payload = {
            "name": name,
            "max_results": max_results,
            "region": region,
            "safesearch": safesearch,
            "timelimit": timelimit,
            "description": description
        }
        
        response = self.session.post(
            f"{self.base_url}/tools/dynamic/duckduckgo",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def create_api_tool(
        self,
        name: str,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        timeout: float = 10.0
    ) -> Dict[str, Any]:
        """
        Quick method to create a REST API tool
        
        Args:
            name: Tool name
            url: Base URL for the API
            method: HTTP method
            headers: HTTP headers
            description: Tool description
            timeout: Request timeout
            
        Returns:
            Created tool definition
        """
        return self.create_from_template(
            template=ToolTemplate.API_REST,
            name=name,
            description=description,
            config_overrides={
                "url": url,
                "method": method,
                "headers": headers or {},
                "timeout": timeout
            }
        )
    
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
        """
        Create a completely custom tool
        
        Args:
            name: Tool name
            tool_type: Type of tool
            config: Tool configuration
            input_schema: JSON schema for inputs
            output_schema: JSON schema for outputs
            description: Tool description
            save_to_disk: Whether to save to disk
            
        Returns:
            Created tool definition
        """
        payload = {
            "name": name,
            "type": tool_type,
            "config": config,
            "input_schema": input_schema,
            "output_schema": output_schema,
            "description": description,
            "save_to_disk": save_to_disk
        }
        
        response = self.session.post(
            f"{self.base_url}/tools/dynamic/custom",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    # ============= Batch Operations =============
    
    def batch_create(
        self,
        tool_specs: List[Dict[str, Any]],
        save_to_disk: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Create multiple tools at once
        
        Args:
            tool_specs: List of tool specifications
            save_to_disk: Whether to save to disk
            
        Returns:
            List of created tools
        """
        payload = {
            "tools": tool_specs,
            "save_to_disk": save_to_disk
        }
        
        response = self.session.post(
            f"{self.base_url}/tools/dynamic/batch",
            json=payload
        )
        response.raise_for_status()
        return response.json()["tools"]
    
    # ============= Recipe Methods =============
    
    def list_recipes(self) -> List[Dict[str, Any]]:
        """
        List all available tool recipes
        
        Returns:
            List of recipe information
        """
        response = self.session.get(f"{self.base_url}/tools/dynamic/recipes")
        response.raise_for_status()
        return response.json()["recipes"]
    
    def create_from_recipe(self, recipe_name: str) -> List[Dict[str, Any]]:
        """
        Create tools from a predefined recipe
        
        Args:
            recipe_name: Name of the recipe
            
        Returns:
            List of created tools
        """
        response = self.session.post(f"{self.base_url}/tools/dynamic/recipes/{recipe_name}")
        response.raise_for_status()
        return response.json()["tools"]
    
    # ============= Tool Management =============
    
    def get_tool(self, tool_id: str) -> Dict[str, Any]:
        """
        Get a specific tool by ID
        
        Args:
            tool_id: Tool identifier
            
        Returns:
            Tool definition
        """
        response = self.session.get(f"{self.base_url}/tools/{tool_id}")
        response.raise_for_status()
        return response.json()
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List all created tools
        
        Returns:
            List of all tools
        """
        response = self.session.get(f"{self.base_url}/tools/")
        response.raise_for_status()
        return response.json()
    
    def delete_tool(self, tool_id: str) -> bool:
        """
        Delete a tool
        
        Args:
            tool_id: Tool identifier
            
        Returns:
            True if deleted successfully
        """
        response = self.session.delete(f"{self.base_url}/tools/{tool_id}")
        response.raise_for_status()
        return response.json().get("deleted", False)


# ============= Helper Builder Classes =============

class SearchToolBuilder:
    """Fluent builder for search tools"""
    
    def __init__(self, client: AgenticToolClient):
        self.client = client
        self.name = "Search Tool"
        self.max_results = 5
        self.region = "wt-wt"
        self.safesearch = "moderate"
        self.timelimit = None
        self.description = None
    
    def with_name(self, name: str) -> 'SearchToolBuilder':
        self.name = name
        return self
    
    def with_max_results(self, count: int) -> 'SearchToolBuilder':
        self.max_results = count
        return self
    
    def with_region(self, region: str) -> 'SearchToolBuilder':
        self.region = region
        return self
    
    def strict_search(self) -> 'SearchToolBuilder':
        self.safesearch = "strict"
        return self
    
    def moderate_search(self) -> 'SearchToolBuilder':
        self.safesearch = "moderate"
        return self
    
    def unsafe_search(self) -> 'SearchToolBuilder':
        self.safesearch = "off"
        return self
    
    def recent_day(self) -> 'SearchToolBuilder':
        self.timelimit = "d"
        return self
    
    def recent_week(self) -> 'SearchToolBuilder':
        self.timelimit = "w"
        return self
    
    def recent_month(self) -> 'SearchToolBuilder':
        self.timelimit = "m"
        return self
    
    def with_description(self, desc: str) -> 'SearchToolBuilder':
        self.description = desc
        return self
    
    def build(self) -> Dict[str, Any]:
        """Create the search tool"""
        return self.client.create_duckduckgo_search(
            name=self.name,
            max_results=self.max_results,
            region=self.region,
            safesearch=self.safesearch,
            timelimit=self.timelimit,
            description=self.description
        )


class APIToolBuilder:
    """Fluent builder for API tools"""
    
    def __init__(self, client: AgenticToolClient):
        self.client = client
        self.name = "API Tool"
        self.url = ""
        self.method = "GET"
        self.headers = {}
        self.description = None
        self.timeout = 10.0
    
    def with_name(self, name: str) -> 'APIToolBuilder':
        self.name = name
        return self
    
    def with_url(self, url: str) -> 'APIToolBuilder':
        self.url = url
        return self
    
    def get(self) -> 'APIToolBuilder':
        self.method = "GET"
        return self
    
    def post(self) -> 'APIToolBuilder':
        self.method = "POST"
        return self
    
    def put(self) -> 'APIToolBuilder':
        self.method = "PUT"
        return self
    
    def delete(self) -> 'APIToolBuilder':
        self.method = "DELETE"
        return self
    
    def with_header(self, key: str, value: str) -> 'APIToolBuilder':
        self.headers[key] = value
        return self
    
    def with_auth_token(self, token: str) -> 'APIToolBuilder':
        self.headers["Authorization"] = f"Bearer {token}"
        return self
    
    def with_timeout(self, seconds: float) -> 'APIToolBuilder':
        self.timeout = seconds
        return self
    
    def with_description(self, desc: str) -> 'APIToolBuilder':
        self.description = desc
        return self
    
    def build(self) -> Dict[str, Any]:
        """Create the API tool"""
        return self.client.create_api_tool(
            name=self.name,
            url=self.url,
            method=self.method,
            headers=self.headers,
            description=self.description,
            timeout=self.timeout
        )


# ============= Example Usage =============

def example_usage():
    """Example usage of the client"""
    
    # Initialize client
    client = AgenticToolClient("http://localhost:8000")
    
    # Simple creation
    search_tool = client.create_duckduckgo_search(
        name="Quick Search",
        max_results=5
    )
    print(f"Created: {search_tool['tool']['id']}")
    
    # Using builder pattern
    news_tool = (
        SearchToolBuilder(client)
        .with_name("News Search")
        .with_max_results(10)
        .recent_day()
        .moderate_search()
        .with_description("Search recent news")
        .build()
    )
    print(f"Created: {news_tool['tool']['id']}")
    
    # API tool with builder
    github_tool = (
        APIToolBuilder(client)
        .with_name("GitHub API")
        .with_url("https://api.github.com")
        .get()
        .with_header("Accept", "application/vnd.github.v3+json")
        .with_timeout(15.0)
        .build()
    )
    print(f"Created: {github_tool['tool']['id']}")
    
    # Batch creation
    tools = client.batch_create([
        {
            "template": "duckduckgo_search",
            "name": "Fast Search",
            "config": {"max_results": 3}
        },
        {
            "template": "duckduckgo_search",
            "name": "Deep Search",
            "config": {"max_results": 15}
        }
    ])
    print(f"Batch created {len(tools)} tools")
    
    # Recipe creation
    web_tools = client.create_from_recipe("web_search")
    print(f"Created {len(web_tools)} tools from recipe")
    
    # List all tools
    all_tools = client.list_tools()
    print(f"Total tools: {len(all_tools)}")


if __name__ == "__main__":
    example_usage()
