# MCP Server Toolkit

A framework for building Model Context Protocol (MCP) servers with pluggable data sources.

## Overview

The MCP Server Toolkit provides a standardized way to create MCP servers that can integrate with various external data sources through a plugin system. This allows AI assistants to access and query data from multiple platforms in a consistent manner.

## Features

- **Plugin Architecture**: Easily extensible through plugins for different data sources
- **Authentication**: Built-in API key authentication for secure access
- **HTTP & stdio modes**: Run as a web server or integrate directly with MCP clients
- **Type Safety**: Built with Python type hints for better development experience
- **Async Support**: Full async/await support for high performance

## Quick Start

### Installation

```bash
pip install mcp-server-toolkit
```

### Basic Usage

```python
from mcp_server_toolkit import MCPServer
from mcp_server_toolkit.plugins import CapsulePlugin

# Create server
server = MCPServer(name="My MCP Server")

# Add plugins
capsule_plugin = CapsulePlugin(config={
    "api_token": "your-capsule-api-token"
})
server.add_plugin(capsule_plugin)

# Run server
server.run_server()  # HTTP mode
# or
server.run_stdio()   # stdio mode for MCP clients
```

### Command Line Usage

```bash
# Run Capsule CRM server in HTTP mode
mcp-server capsule http --host 0.0.0.0 --port 8000

# Run in stdio mode for MCP client integration
mcp-server capsule stdio
```

## Available Plugins

### Capsule CRM Plugin

The Capsule CRM plugin provides read-only access to Capsule CRM data.

**Configuration:**
- `api_token`: Your Capsule API token (or set `CAPSULE_API_TOKEN` env var)
- `base_url`: Capsule API base URL (optional, defaults to https://api.capsulecrm.com/api/v2)

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

### Creating a Custom Plugin

```python
from mcp_server_toolkit import BasePlugin
from fastmcp import FastMCP
from typing import Dict, Any

class MyCustomPlugin(BasePlugin):
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("My Custom Plugin", config)
        # Plugin initialization
    
    async def initialize(self) -> None:
        """Initialize plugin resources"""
        pass
    
    async def cleanup(self) -> None:
        """Clean up plugin resources"""
        pass
    
    async def authenticate(self) -> bool:
        """Authenticate with external service"""
        return True
    
    def register_tools(self, mcp: FastMCP) -> None:
        """Register tools with MCP server"""
        
        @mcp.tool
        async def my_tool(param: str) -> Dict[str, Any]:
            """My custom tool description"""
            # Tool implementation
            return {"result": f"Processed {param}"}
```

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

The toolkit is built around several key components:

- **MCPServer**: Main server class that manages plugins and handles requests
- **BasePlugin**: Abstract base class for all plugins
- **Authentication**: Middleware for API key authentication
- **Plugin System**: Dynamic plugin loading and tool registration

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