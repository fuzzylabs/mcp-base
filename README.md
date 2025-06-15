# MCP Server Toolkit

A library for building Model Context Protocol (MCP) servers using common patterns extracted from real-world implementations.

## Overview

The MCP Server Toolkit provides reusable components and patterns to quickly build MCP servers for different APIs and data sources. It extracts common functionality like authentication, pagination, error handling, and server setup into a clean library that follows the same patterns used in successful MCP implementations.

## Features

- **Library Architecture**: Reusable components and base classes for quick MCP server development
- **API Client Abstraction**: Built-in HTTP client with authentication and error handling
- **Common Patterns**: Pagination, search, filtering utilities extracted from real implementations
- **Authentication**: Multiple auth strategies (Bearer tokens, API keys)
- **HTTP & stdio modes**: Run as a web server or integrate directly with MCP clients
- **Type Safety**: Built with Python type hints for better development experience
- **Async Support**: Full async/await support for high performance

## Quick Start

### Installation

```bash
pip install mcp-server-toolkit
```

### Using the Built-in Capsule Server

```python
from mcp_server_toolkit import CapsuleMCPServer

# Create and run Capsule CRM server
server = CapsuleMCPServer(
    api_token="your-capsule-api-token",
    mcp_api_key="your-mcp-api-key"
)

server.run_server()  # HTTP mode
# or
server.run_stdio()   # stdio mode for MCP clients
```

### Building a Custom Server

```python
from mcp_server_toolkit import BaseMCPServer, BearerTokenAPIClient, paginated_endpoint

class MyMCPServer(BaseMCPServer):
    def __init__(self, api_token: str, mcp_api_key: str = None):
        api_client = BearerTokenAPIClient(
            base_url="https://api.example.com/v1",
            api_token=api_token
        )
        
        super().__init__(
            name="My MCP Server",
            api_client=api_client,
            mcp_api_key=mcp_api_key
        )
    
    def register_tools(self):
        @self.mcp.tool
        @paginated_endpoint()
        async def list_items(page: int = 1, per_page: int = 50):
            """List items with automatic pagination."""
            return await self.api_client.get("items", params={
                "page": page,
                "per_page": per_page
            })

# Use your server
server = MyMCPServer(api_token="your-token")
server.run_server()
```

### Command Line Usage

```bash
# Run Capsule CRM server in HTTP mode
mcp-server capsule http --host 0.0.0.0 --port 8000

# Run in stdio mode for MCP client integration
mcp-server capsule stdio
```

## Library Components

### Base Classes

- **`BaseMCPServer`**: Abstract base class for MCP servers with common functionality
- **`BaseAPIClient`**: HTTP client base class with authentication and error handling
- **`BearerTokenAPIClient`**: API client for Bearer token authentication
- **`APIKeyClient`**: API client for API key authentication

### Utilities

- **`@paginated_endpoint`**: Decorator for handling pagination parameters
- **`build_api_params()`**: Helper to build API parameter dictionaries
- **`build_search_params()`**: Helper for search endpoint parameters
- **`build_filter_query()`**: Helper for complex API filtering
- **`MCPToolRegistry`**: Tool organization and categorization
- **`require_env_var()`**: Environment variable validation with test support

### Built-in Servers

#### Capsule CRM Server

Complete MCP server for Capsule CRM with 25+ tools.

**Available Tools:**
- `list_contacts`: Get paginated list of contacts
- `search_contacts`: Search contacts by keyword
- `list_recent_contacts`: Get recently contacted contacts
- `list_opportunities`: Get paginated list of opportunities
- `list_open_opportunities`: Get open opportunities
- `list_cases`: Get support cases
- `search_cases`: Search cases by keyword
- `get_case`: Get specific case details
- `list_tasks`: Get tasks
- `get_task`: Get specific task details
- `list_entries`: Get timeline entries
- `get_entry`: Get specific entry details
- `list_projects`: Get projects
- `get_project`: Get specific project details
- `list_tags`: Get tags
- `get_tag`: Get specific tag details
- `list_users`: Get users
- `get_user`: Get specific user details
- `get_contact`: Get specific contact details
- `get_opportunity`: Get specific opportunity details
- `list_pipelines`: Get sales pipelines
- `list_stages`: Get pipeline stages
- `list_milestones`: Get opportunity milestones
- `list_custom_fields`: Get custom field definitions
- `list_products`: Get products
- `list_categories`: Get product categories
- `list_currencies`: Get supported currencies

## Configuration

### Environment Variables

- `MCP_API_KEY`: API key for authenticating requests to MCP endpoints
- `CAPSULE_API_TOKEN`: Capsule CRM API token
- `CAPSULE_BASE_URL`: Capsule CRM API base URL (optional)

### Example .env file

```env
MCP_API_KEY=your-mcp-api-key
CAPSULE_API_TOKEN=your-capsule-api-token
CAPSULE_BASE_URL=https://api.capsulecrm.com/api/v2
```

## Development

### Building a Custom MCP Server

The toolkit makes it easy to build new MCP servers by providing common patterns:

```python
from mcp_server_toolkit import (
    BaseMCPServer, 
    BearerTokenAPIClient,
    paginated_endpoint,
    build_api_params
)

class GitHubMCPServer(BaseMCPServer):
    def __init__(self, github_token: str, mcp_api_key: str = None):
        api_client = BearerTokenAPIClient(
            base_url="https://api.github.com",
            api_token=github_token,
            user_agent="my-github-mcp-server/1.0"
        )
        
        super().__init__(
            name="GitHub MCP Server",
            api_client=api_client,
            mcp_api_key=mcp_api_key
        )
    
    async def test_connection(self) -> bool:
        """Test GitHub API connection."""
        try:
            await self.api_client.get("user")
            return True
        except:
            return False
    
    def register_tools(self):
        @self.mcp.tool
        @paginated_endpoint()
        async def list_repos(
            page: int = 1, 
            per_page: int = 30,
            org: str = None
        ):
            """List repositories."""
            endpoint = f"orgs/{org}/repos" if org else "user/repos"
            params = build_api_params(page=page, per_page=per_page)
            return await self.api_client.get(endpoint, params=params)
        
        @self.mcp.tool
        async def get_repo(owner: str, repo: str):
            """Get repository details."""
            return await self.api_client.get(f"repos/{owner}/{repo}")
```

### Common Patterns

The toolkit includes utilities for common API patterns:

- **Pagination**: Use `@paginated_endpoint()` decorator and `build_api_params()`
- **Search**: Use `build_search_params()` for search endpoints
- **Filtering**: Use `build_filter_query()` for complex filters
- **Authentication**: Choose from `BearerTokenAPIClient` or `APIKeyClient`
- **Error Handling**: Built into the base API client

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Quality

```bash
# Format code
black mcp_server_toolkit/
isort mcp_server_toolkit/

# Lint code
ruff mcp_server_toolkit/

# Type checking
mypy mcp_server_toolkit/
```

## Architecture

The toolkit provides a layered architecture for building MCP servers:

```
┌─────────────────────────────────────┐
│          Your MCP Server            │  ← Inherit from BaseMCPServer
│  (e.g., GitHubMCPServer)           │
├─────────────────────────────────────┤
│         BaseMCPServer              │  ← Base class with common functionality
│  • FastMCP integration            │
│  • Authentication middleware       │
│  • HTTP + stdio modes             │
├─────────────────────────────────────┤
│        API Client Layer            │  ← HTTP client abstraction
│  • BearerTokenAPIClient           │
│  • APIKeyClient                   │
│  • Error handling                 │
├─────────────────────────────────────┤
│          Utilities                 │  ← Common patterns and helpers
│  • Pagination decorator           │
│  • Parameter builders             │
│  • Environment helpers            │
└─────────────────────────────────────┘
```

### Key Benefits

- **Rapid Development**: Start with working patterns from real implementations
- **Consistency**: All servers follow the same architecture
- **Reusability**: Common code extracted into the library
- **Maintainability**: Clear separation of concerns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Links

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Capsule CRM API Documentation](https://developer.capsulecrm.com/)