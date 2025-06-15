# MCP Server Generation Guide

This guide provides detailed instructions for generating new MCP servers using the mcp-base library. Follow these patterns to ensure consistency and best practices across all generated projects.

## Project Generation Process

### 1. Information Gathering

Before generating a new MCP server, gather the following information:

**Required Variables:**
- `PROJECT_NAME`: Package name (e.g., "salesforce-mcp", "hubspot-mcp")
- `PROJECT_TITLE`: Human-readable title (e.g., "Salesforce MCP Server")
- `PROJECT_DESCRIPTION`: Brief description for pyproject.toml and README
- `SERVICE_NAME`: Name of the external service (e.g., "Salesforce", "HubSpot")
- `SERVICE_NAME_LOWER`: Lowercase service name (e.g., "salesforce", "hubspot")
- `PACKAGE_NAME`: Python package name (e.g., "salesforce_mcp", "hubspot_mcp")
- `SERVER_CLASS_NAME`: Main server class name (e.g., "SalesforceMCPServer", "HubSpotMCPServer")
- `API_BASE_URL`: Base URL for the service API
- `API_TOKEN_ENV_VAR`: Environment variable name for API token (e.g., "SALESFORCE_API_TOKEN")
- `CLI_NAME`: Command line script name (e.g., "salesforce-mcp", "hubspot-mcp")
- `AUTHOR_NAME`: Author name for pyproject.toml
- `AUTHOR_EMAIL`: Author email for pyproject.toml
- `HOMEPAGE_URL`: GitHub repository URL
- `REPO_URL`: Full repository clone URL

### 2. Directory Structure Creation

Create the following directory structure:

```
{PROJECT_NAME}/
├── {PACKAGE_NAME}/
│   ├── __init__.py
│   ├── server.py
│   └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_server.py
├── .github/
│   └── workflows/
│       ├── test.yml
│       └── publish.yml
├── pyproject.toml
├── README.md
├── .env.example
├── pytest.ini
├── Makefile
├── LICENCE
└── .gitignore
```

### 3. Template Processing

Copy all files from the `templates/` directory and replace template variables:

1. **Copy template files** from mcp-base repository
2. **Replace template variables** using the gathered information
3. **Rename template directories** (e.g., `{{PACKAGE_NAME}}` → actual package name)
4. **Remove `.template` extensions** from filenames

### 4. Variable Substitution Examples

```python
# Example variable substitutions for Salesforce MCP Server:
{
    "PROJECT_NAME": "salesforce-mcp",
    "PROJECT_TITLE": "Salesforce MCP Server", 
    "PROJECT_DESCRIPTION": "Model Context Protocol server for Salesforce CRM",
    "SERVICE_NAME": "Salesforce",
    "SERVICE_NAME_LOWER": "salesforce",
    "PACKAGE_NAME": "salesforce_mcp",
    "SERVER_CLASS_NAME": "SalesforceMCPServer",
    "API_BASE_URL": "https://api.salesforce.com/v1",
    "API_TOKEN_ENV_VAR": "SALESFORCE_API_TOKEN",
    "CLI_NAME": "salesforce-mcp",
    "AUTHOR_NAME": "Your Name",
    "AUTHOR_EMAIL": "your.email@example.com",
    "HOMEPAGE_URL": "https://github.com/yourorg/salesforce-mcp",
    "REPO_URL": "https://github.com/yourorg/salesforce-mcp.git"
}
```

## Development Workflow Rules

When adding new features to generated MCP servers, ALWAYS follow these rules:

### Adding New Tools

1. **Add the tool to `server.py`**:
   ```python
   @self.mcp.tool
   @paginated_endpoint()  # Use decorator for paginated endpoints
   async def new_tool_name(param1: type, param2: type = default) -> Dict[str, Any]:
       """Clear description of what the tool does.
       
       Args:
           param1: Description of param1
           param2: Description of param2 with default value
       """
       # Implementation using self.api_client
       return await self.api_client.get("endpoint", params=build_api_params(...))
   ```

2. **Add corresponding test in `tests/test_server.py`**:
   ```python
   @pytest.mark.asyncio
   async def test_new_tool_name():
       """Test the new_tool_name function."""
       with patch.dict(os.environ, {"{API_TOKEN_ENV_VAR}": "test-token"}):
           server = {SERVER_CLASS_NAME}(api_token="test-token")
           
           # Mock API response
           mock_response = {"expected": "response"}
           server.api_client.get = AsyncMock(return_value=mock_response)
           
           # Test implementation
           # (You'll need to find a way to call the tool through MCP)
   ```

3. **Update README.md Available Tools section**:
   ```markdown
   ## Available Tools
   
   - `existing_tool`: Description
   - `new_tool_name`: Description of the new tool
   ```

4. **Update CLI help if applicable** in `cli.py`

5. **Run tests and ensure they pass**:
   ```bash
   pytest
   ```

### Code Quality Requirements

1. **Type Hints**: All functions must have complete type hints
2. **Docstrings**: All tools must have detailed docstrings with Args descriptions
3. **Error Handling**: Use the base API client's built-in error handling
4. **Pagination**: Use `@paginated_endpoint()` decorator for paginated endpoints
5. **Parameter Building**: Use `build_api_params()` helper for query parameters

### Testing Requirements

1. **Mock API calls** using `AsyncMock`
2. **Test both success and failure cases**
3. **Use environment variable patching** for API tokens
4. **Test parameter validation**
5. **Achieve reasonable test coverage**

## Common Patterns

### Authentication Patterns

**Bearer Token (most common):**
```python
api_client = BearerTokenAPIClient(
    base_url=base_url,
    api_token=api_token,
    user_agent=f"{PROJECT_NAME}/0.1.0"
)
```

**API Key Header:**
```python
api_client = APIKeyClient(
    base_url=base_url,
    api_token=api_token,
    api_key_header="X-API-Key",  # Custom header name
    user_agent=f"{PROJECT_NAME}/0.1.0"
)
```

### Tool Patterns

**Simple GET endpoint:**
```python
@self.mcp.tool
async def get_item(item_id: int) -> Dict[str, Any]:
    """Get a specific item."""
    return await self.api_client.get(f"items/{item_id}")
```

**Paginated list endpoint:**
```python
@self.mcp.tool
@paginated_endpoint()
async def list_items(
    page: int = 1,
    per_page: int = 50,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """List items with pagination."""
    params = build_api_params(page=page, per_page=per_page, category=category)
    return await self.api_client.get("items", params=params)
```

**Search endpoint:**
```python
@self.mcp.tool
async def search_items(query: str, limit: int = 20) -> Dict[str, Any]:
    """Search for items."""
    params = build_search_params(query, per_page=limit)
    return await self.api_client.get("items/search", params=params)
```

**POST endpoint with data:**
```python
@self.mcp.tool
async def create_item(name: str, description: str) -> Dict[str, Any]:
    """Create a new item."""
    data = {"name": name, "description": description}
    return await self.api_client.post("items", json=data)
```

### Error Handling

The base API client handles most errors automatically. For custom error handling:

```python
try:
    result = await self.api_client.get("endpoint")
    return result
except RuntimeError as e:
    # Log error or handle specifically
    raise  # Re-raise to let MCP framework handle
```

## Version Management

### Initial Version
- Start all new projects at version `0.1.0`
- Use semantic versioning: `MAJOR.MINOR.PATCH`

### Updating Dependencies
- Keep `mcp-base` dependency up to date
- Update in pyproject.toml: `mcp-base>=X.Y.Z`
- Test thoroughly after updates

### Release Process
1. Update version in `pyproject.toml` and `__init__.py`
2. Update `CHANGELOG.md` if present
3. Create GitHub release
4. GitHub Actions will automatically publish to PyPI

## Quality Checklist

Before considering a generated MCP server complete:

- [ ] All templates processed correctly
- [ ] Tests pass: `pytest`
- [ ] Linting passes: `ruff check package_name/`
- [ ] Type checking passes: `mypy package_name/`
- [ ] Code formatted: `black package_name/ tests/`
- [ ] Imports sorted: `isort package_name/ tests/`
- [ ] README.md updated with actual tool descriptions
- [ ] Environment variables documented
- [ ] CLI commands work correctly
- [ ] HTTP and stdio modes both functional
- [ ] API connection test works
- [ ] At least 2-3 meaningful tools implemented

## Advanced Patterns

### Custom API Client
If the service uses non-standard authentication:

```python
class CustomAPIClient(BaseAPIClient):
    def get_auth_headers(self) -> Dict[str, str]:
        # Implement custom authentication
        return {"Custom-Auth": f"scheme {self.api_token}"}

# Use in server:
api_client = CustomAPIClient(base_url, api_token)
```

### Complex Filtering
For services with advanced filtering:

```python
@self.mcp.tool
async def list_items_filtered(
    status: Optional[str] = None,
    created_after: Optional[str] = None,
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """List items with complex filtering."""
    filter_conditions = []
    
    if status:
        filter_conditions.append({"field": "status", "operator": "eq", "value": status})
    if created_after:
        filter_conditions.append({"field": "created_at", "operator": "gte", "value": created_after})
    if tags:
        filter_conditions.append({"field": "tags", "operator": "in", "value": tags})
    
    filter_data = build_filter_query(
        conditions=filter_conditions,
        order_by=[{"field": "created_at", "direction": "desc"}]
    )
    
    return await self.api_client.post("items/filter", json=filter_data)
```

## Evolution and Updates

When the mcp-base library evolves:

1. **Update dependency** in pyproject.toml
2. **Review breaking changes** in mcp-base changelog  
3. **Update imports** if API changes
4. **Run tests** to ensure compatibility
5. **Update patterns** to use new features
6. **Regenerate project files** if major template updates available

This ensures all MCP servers benefit from improvements to the base library while maintaining compatibility and consistency.