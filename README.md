# MCP Base

A foundational Python library for building Model Context Protocol (MCP) servers. Transform any API into an AI-accessible service with proven patterns and reusable components.

## Key Features

- **Base Classes**: Inherit from `BaseMCPServer` for rapid MCP server development
- **Authentication**: Built-in support for Bearer tokens, API keys, and custom auth
- **Project Templates**: Complete boilerplate with tests, CI/CD, and documentation
- **Utilities**: Pagination decorators, parameter builders, and common patterns
- **Future-Proof**: Automatic benefits from library improvements and new features

## Quick Start

```bash
pip install mcp-base
```

```python
from mcp_base import BaseMCPServer, BearerTokenAPIClient

class MyMCPServer(BaseMCPServer):
    def __init__(self, api_token: str):
        api_client = BearerTokenAPIClient(
            base_url="https://api.example.com",
            api_token=api_token
        )
        super().__init__("My Server", api_client)
    
    def register_tools(self):
        @self.mcp.tool
        async def get_data(id: str):
            """Get data by ID."""
            return await self.api_client.get(f"data/{id}")

server = MyMCPServer("your-token")
server.run()
```

## Project Templates

Generate complete MCP server projects using the templates in `templates/`. See [CLAUDE.md](./CLAUDE.md) for detailed generation instructions.

## Core Components

- **`BaseMCPServer`** - Abstract base class for MCP servers
- **`BaseAPIClient`** - HTTP client with authentication and error handling
- **`BearerTokenAPIClient`** - Bearer token authentication
- **`APIKeyClient`** - API key authentication
- **`@paginated_endpoint`** - Automatic pagination decorator
- **`build_api_params()`** - Parameter dictionary construction
- **`build_filter_query()`** - Complex filtering and sorting
- **`MCPToolRegistry`** - Tool organisation and management

## Authentication

**Bearer Token (Recommended)**
```python
api_client = BearerTokenAPIClient("https://api.service.com", "your-token")
```

**API Key**
```python
api_client = APIKeyClient("https://api.service.com", "your-key", api_key_header="X-API-Key")
```

**Custom Authentication**
```python
class CustomAuthClient(BaseAPIClient):
    def get_auth_headers(self):
        return {"Authorization": f"Custom {self.api_token}"}
```

## Advanced Patterns

See `examples/` directory for complete implementations of:
- **Pagination** - `@paginated_endpoint` decorator with automatic parameter handling
- **Complex Filtering** - Multi-condition search with `build_filter_query()`
- **Error Handling** - Graceful API error management
- **Tool Organisation** - Registry patterns for large servers

## Evolution Architecture

MCP Base implements a **shared evolution model** - all servers automatically benefit from library improvements:

```
                    Automatic Benefits
mcp-base library ─────────────────────► All MCP servers
     │
     ├─ Performance optimisations ─────► Faster response times
     ├─ New authentication methods ────► OAuth, SSO support  
     ├─ Container deployment ──────────► Docker, Kubernetes
     ├─ Monitoring & logging ──────────► Observability tools
     └─ Security enhancements ─────────► Latest best practices
```

This follows proven patterns from successful frameworks like [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/), which demonstrate how foundational libraries can evolve while maintaining backward compatibility and automatically improving all dependent projects.

**Examples**: When MCP Base adds OAuth support, all existing servers inherit it. Performance optimisations boost every server without code changes.

## Example MCP Servers

- **[Capsule CRM](https://github.com/fuzzylabs/capsule-mcp)** - Customer relationship management integration

## Development

**Contributing to MCP Base**
```bash
git clone https://github.com/fuzzylabs/mcp-base.git
cd mcp-base
pip install -e ".[dev]"
pytest
```

**Building MCP Servers**
```bash
# Use templates to generate new servers (see CLAUDE.md)
cd your-new-mcp-server/
uv sync --dev
uv run your-server-name
```

## Documentation

- **[MCP Specification](https://spec.modelcontextprotocol.io/)** - Official Model Context Protocol docs
- **[FastMCP](https://github.com/jlowin/fastmcp)** - Underlying MCP framework
- **[Examples](./examples/)** - Working code samples and patterns
- **[Templates](./templates/)** - Project generation boilerplate

## Licence

MIT