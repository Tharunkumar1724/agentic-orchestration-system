"""
Interactive Tool Creator
Simple CLI for creating tools without code
"""

from agentic_tool_client import AgenticToolClient, SearchToolBuilder, APIToolBuilder
import sys


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*70)
    print(text.center(70))
    print("="*70 + "\n")


def print_menu(title, options):
    """Print a menu"""
    print(f"\n{title}")
    print("-" * len(title))
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print()


def get_choice(prompt, max_choice):
    """Get user choice"""
    while True:
        try:
            choice = int(input(f"{prompt} (1-{max_choice}): "))
            if 1 <= choice <= max_choice:
                return choice
            print(f"Please enter a number between 1 and {max_choice}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)


def get_input(prompt, default=None):
    """Get user input with optional default"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    try:
        value = input(prompt).strip()
        return value if value else default
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)


def create_duckduckgo_tool(client):
    """Interactive DuckDuckGo tool creation"""
    print_header("🔍 Create DuckDuckGo Search Tool")
    
    name = get_input("Tool name", "My Search Tool")
    description = get_input("Description (optional)")
    
    # Max results
    print("\nHow many results?")
    print("  1. Quick (3 results)")
    print("  2. Standard (5 results)")
    print("  3. Detailed (10 results)")
    print("  4. Comprehensive (15 results)")
    print("  5. Custom")
    
    choice = get_choice("Choose option", 5)
    max_results = {1: 3, 2: 5, 3: 10, 4: 15}.get(choice)
    if choice == 5:
        max_results = int(get_input("Enter number of results", "5"))
    
    # Region
    print("\nSelect region:")
    print("  1. Global (wt-wt)")
    print("  2. United States (us-en)")
    print("  3. United Kingdom (uk-en)")
    print("  4. Germany (de-de)")
    print("  5. Custom")
    
    choice = get_choice("Choose region", 5)
    regions = {1: "wt-wt", 2: "us-en", 3: "uk-en", 4: "de-de"}
    region = regions.get(choice)
    if choice == 5:
        region = get_input("Enter region code", "wt-wt")
    
    # Safety
    print("\nSafety level:")
    print("  1. Strict")
    print("  2. Moderate")
    print("  3. Off")
    
    choice = get_choice("Choose safety", 3)
    safesearch = {1: "strict", 2: "moderate", 3: "off"}[choice]
    
    # Time limit
    print("\nTime range:")
    print("  1. All time")
    print("  2. Last day")
    print("  3. Last week")
    print("  4. Last month")
    
    choice = get_choice("Choose time range", 4)
    timelimit = {1: None, 2: "d", 3: "w", 4: "m"}[choice]
    
    # Create the tool
    print("\n⏳ Creating tool...")
    try:
        result = client.create_duckduckgo_search(
            name=name,
            max_results=max_results,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            description=description
        )
        
        tool_id = result["tool"]["id"]
        print(f"\n✅ Success! Created tool: {tool_id}")
        print(f"   Name: {name}")
        print(f"   Max Results: {max_results}")
        print(f"   Region: {region}")
        print(f"   Safety: {safesearch}")
        print(f"   Time Limit: {timelimit or 'None'}")
        
        return tool_id
    except Exception as e:
        print(f"\n❌ Error creating tool: {str(e)}")
        return None


def create_api_tool(client):
    """Interactive API tool creation"""
    print_header("🌐 Create API Tool")
    
    name = get_input("Tool name", "My API Tool")
    url = get_input("API URL", "https://api.example.com")
    description = get_input("Description (optional)")
    
    # Method
    print("\nHTTP Method:")
    print("  1. GET")
    print("  2. POST")
    print("  3. PUT")
    print("  4. DELETE")
    
    choice = get_choice("Choose method", 4)
    method = {1: "GET", 2: "POST", 3: "PUT", 4: "DELETE"}[choice]
    
    # Headers
    print("\nAdd custom headers? (y/n)")
    add_headers = get_input("", "n").lower() == "y"
    
    headers = {}
    if add_headers:
        print("\nEnter headers (empty to finish):")
        while True:
            key = get_input("Header name (empty to finish)")
            if not key:
                break
            value = get_input(f"Value for {key}")
            headers[key] = value
    
    # Timeout
    timeout = float(get_input("Timeout in seconds", "10"))
    
    # Create the tool
    print("\n⏳ Creating tool...")
    try:
        result = client.create_api_tool(
            name=name,
            url=url,
            method=method,
            headers=headers,
            description=description,
            timeout=timeout
        )
        
        tool_id = result["tool"]["id"]
        print(f"\n✅ Success! Created tool: {tool_id}")
        print(f"   Name: {name}")
        print(f"   URL: {url}")
        print(f"   Method: {method}")
        print(f"   Timeout: {timeout}s")
        
        return tool_id
    except Exception as e:
        print(f"\n❌ Error creating tool: {str(e)}")
        return None


def create_from_template(client):
    """Interactive template-based creation"""
    print_header("📋 Create from Template")
    
    # List templates
    templates = client.list_templates()
    
    print("Available templates:")
    for i, template in enumerate(templates, 1):
        print(f"  {i}. {template['template']} ({template['type']})")
    
    choice = get_choice("Choose template", len(templates))
    template_name = templates[choice - 1]["template"]
    
    # Get template schema
    schema = client.get_template_schema(template_name)
    
    print(f"\nCreating tool from '{template_name}' template")
    print(f"Type: {schema['type']}")
    
    name = get_input("Tool name")
    description = get_input("Description (optional)")
    
    # For simplicity, just create with defaults
    # In a full version, we'd prompt for each config option
    
    print("\n⏳ Creating tool...")
    try:
        result = client.create_from_template(
            template=template_name,
            name=name,
            description=description
        )
        
        tool_id = result["tool"]["id"]
        print(f"\n✅ Success! Created tool: {tool_id}")
        
        return tool_id
    except Exception as e:
        print(f"\n❌ Error creating tool: {str(e)}")
        return None


def list_tools(client):
    """List all created tools"""
    print_header("📚 Your Tools")
    
    try:
        tools = client.list_tools()
        
        if not tools:
            print("No tools created yet.")
            return
        
        print(f"Found {len(tools)} tools:\n")
        
        for i, tool in enumerate(tools, 1):
            print(f"{i}. {tool.get('name', 'Unnamed')} ({tool.get('id', 'unknown')})")
            print(f"   Type: {tool.get('type', 'unknown')}")
            if tool.get('description'):
                print(f"   Description: {tool['description']}")
            print()
        
    except Exception as e:
        print(f"❌ Error listing tools: {str(e)}")


def create_from_recipe(client):
    """Create tools from a recipe"""
    print_header("🍳 Create from Recipe")
    
    try:
        recipes = client.list_recipes()
        
        print("Available recipes:\n")
        for i, recipe in enumerate(recipes, 1):
            print(f"{i}. {recipe['name']}")
            print(f"   {recipe['description']}")
            print(f"   Creates {recipe['tool_count']} tools\n")
        
        choice = get_choice("Choose recipe", len(recipes))
        recipe_name = recipes[choice - 1]["name"]
        
        print(f"\n⏳ Creating tools from '{recipe_name}' recipe...")
        
        result = client.create_from_recipe(recipe_name)
        
        print(f"\n✅ Success! Created {len(result)} tools:")
        for tool in result:
            print(f"   • {tool['name']} ({tool['id']})")
        
    except Exception as e:
        print(f"\n❌ Error creating from recipe: {str(e)}")


def main():
    """Main interactive loop"""
    print_header("🛠️  AgenticApp Tool Creator")
    
    # Initialize client
    base_url = get_input("Backend URL", "http://localhost:8000")
    client = AgenticToolClient(base_url)
    
    print("\n✅ Connected to backend")
    
    while True:
        print_menu(
            "Main Menu",
            [
                "Create DuckDuckGo Search Tool",
                "Create API Tool",
                "Create from Template",
                "Create from Recipe",
                "List My Tools",
                "Exit"
            ]
        )
        
        choice = get_choice("Choose option", 6)
        
        if choice == 1:
            create_duckduckgo_tool(client)
        elif choice == 2:
            create_api_tool(client)
        elif choice == 3:
            create_from_template(client)
        elif choice == 4:
            create_from_recipe(client)
        elif choice == 5:
            list_tools(client)
        elif choice == 6:
            print("\n👋 Goodbye!")
            break
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)
