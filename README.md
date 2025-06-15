# MCP Base

A foundational library for building Model Context Protocol (MCP) servers using proven patterns extracted from real-world implementations.

## Overview

MCP Base provides reusable components and patterns to quickly build MCP servers for different APIs and data sources. It extracts common functionality like authentication, pagination, error handling, and server setup into a clean library that follows the same patterns used in successful MCP implementations.

Rather than a plugin system, MCP Base is a **foundational library** that you import and build upon. Each MCP server remains its own focused project while benefiting from shared infrastructure and evolving best practices.

## Features

- **Foundational Library**: Base classes and utilities for rapid MCP server development
- **Project Templates**: Complete boilerplate for generating new MCP servers
- **API Client Abstraction**: Built-in HTTP client with authentication and error handling
- **Common Patterns**: Pagination, search, filtering utilities extracted from real implementations
- **Multiple Auth Strategies**: Bearer tokens, API keys, custom authentication
- **Development Infrastructure**: Testing, linting, CI/CD templates
- **Evolution Strategy**: All servers benefit from library improvements

## Quick Start

### For Building New MCP Servers

```python
from mcp_base import BaseMCPServer, BearerTokenAPIClient, paginated_endpoint

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

### Using Project Templates

MCP Base includes complete project templates for generating new MCP servers:

```
templates/
├── pyproject.toml.template      # Python project configuration
├── README.md.template           # Documentation template
├── {{PACKAGE_NAME}}/            # Source code templates
├── tests/                       # Test templates
├── .github/workflows/           # CI/CD templates
└── development files...         # Makefile, pytest.ini, etc.
```

See `CLAUDE.md` for detailed generation instructions.

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

## Evolution Strategy

MCP Base follows a **shared evolution model** where improvements to the foundational library automatically benefit all MCP servers built on it:

```
mcp-base (library) ─┬─ Evolution ──→ All servers benefit
                    │
                    ├─ capsule-mcp ──→ Uses mcp-base
                    ├─ salesforce-mcp ──→ Uses mcp-base  
                    ├─ hubspot-mcp ──→ Uses mcp-base
                    └─ your-mcp ──→ Uses mcp-base
```

### Benefits

- **Future-Proof**: Servers inherit improvements automatically
- **Consistent Evolution**: All servers move forward together  
- **Low Migration Cost**: Changes happen in the library, not every server
- **Best Practice Propagation**: New patterns flow to all implementations
- **Community Learning**: Everyone benefits from collective improvements

### Migration Examples

**Container Support**: When MCP Base adds containerization support, all existing servers can adopt it by updating their base class and adding a Dockerfile.

**New Authentication**: When MCP Base adds OAuth support, all servers get access to the new `OAuthAPIClient` class.

**Performance Improvements**: Optimizations in the base HTTP client automatically improve all servers.

## Inspired By Successful Frameworks

This evolution approach follows patterns proven by frameworks like [FastAPI](https://fastapi.tiangolo.com/) and [Next.js](https://nextjs.org/), where improvements to the core framework automatically benefit all applications built on it.

## Examples

### Minimal Server
```python
# examples/minimal_server.py - Basic MCP server
from mcp_base import BaseMCPServer, BearerTokenAPIClient

class MinimalMCPServer(BaseMCPServer):
    # Simple implementation with basic tools
```

### Authentication Patterns
```python
# examples/auth_patterns.py - Different auth strategies
BearerTokenAPIClient()  # Most common
APIKeyClient()          # For API key auth
CustomAuthClient()      # Custom authentication
```

### Advanced Patterns
```python
# examples/advanced_patterns.py - Complex use cases
@paginated_endpoint()    # Automatic pagination
build_filter_query()    # Complex filtering
MCPToolRegistry()       # Tool organization
```

## Real-World Usage

MCP Base is extracted from and powers production MCP servers:

- **capsule-mcp**: Capsule CRM integration (original implementation)
- **Future servers**: Salesforce, HubSpot, GitHub, and more

Each server is its own focused project while sharing the foundational library.

## Development

### Installation

```bash
pip install mcp-base
```

### Running Examples

```bash
# Try the minimal server
python examples/minimal_server.py

# Explore authentication patterns  
python examples/auth_patterns.py

# See advanced patterns
python examples/advanced_patterns.py
```

### Building New Servers

1. **Use Templates**: Copy from `templates/` directory
2. **Follow CLAUDE.md**: Detailed generation guide
3. **Import mcp-base**: Build on the foundational library
4. **Focus on Business Logic**: Let the library handle infrastructure

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Code Quality

```bash
# Format code
black mcp_base/ tests/ examples/
isort mcp_base/ tests/ examples/

# Lint code
ruff check mcp_base/

# Type checking
mypy mcp_base/
```

## Architecture

```
┌─────────────────────────────────────┐
│          Your MCP Server            │  ← Inherit from BaseMCPServer
│  (e.g., SalesforceMCPServer)       │
├─────────────────────────────────────┤
│         BaseMCPServer               │  ← Base class with common functionality
│  • FastMCP integration             │
│  • Authentication middleware        │
│  • HTTP + stdio modes              │
├─────────────────────────────────────┤
│        API Client Layer             │  ← HTTP client abstraction
│  • BearerTokenAPIClient            │
│  • APIKeyClient                    │
│  • Error handling                  │
├─────────────────────────────────────┤
│          Utilities                  │  ← Common patterns and helpers
│  • Pagination decorator            │
│  • Parameter builders              │
│  • Environment helpers             │
└─────────────────────────────────────┘
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

Improvements to MCP Base benefit the entire ecosystem of MCP servers!

## License

MIT License - see LICENSE file for details.

## Links

- [Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Project Templates](./templates/)
- [Generation Guide](./CLAUDE.md)