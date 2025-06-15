# MCP Base - Model Context Protocol Server Library

Build powerful MCP servers rapidly with proven patterns and reusable components. MCP Base is the foundational Python library for creating Model Context Protocol servers that connect AI assistants to external APIs and data sources.

## What is MCP Base?

MCP Base is a comprehensive Python library that provides everything needed to build production-ready Model Context Protocol (MCP) servers. Extract common functionality like authentication, pagination, error handling, and server setup with battle-tested patterns from real-world MCP implementations.

**Transform any API into an AI-accessible service in minutes, not hours.**

## Key Features

- **🚀 Rapid Development**: Pre-built base classes and utilities for instant MCP server creation
- **📋 Complete Project Templates**: Full boilerplate including tests, CI/CD, documentation
- **🔐 Multiple Authentication**: Bearer tokens, API keys, custom authentication strategies
- **📄 Automatic Pagination**: Built-in decorators for handling paginated API responses
- **🛠️ Development Tools**: Testing frameworks, linting, type checking, CI/CD workflows
- **🔄 Future-Proof Architecture**: Benefit automatically from library improvements and new features
- **📚 Production-Ready**: Extracted from live MCP servers handling real workloads

## Quick Start Guide

### Installation

```bash
pip install mcp-base
```

### Create Your First MCP Server

```python
from mcp_base import BaseMCPServer, BearerTokenAPIClient, paginated_endpoint

class GitHubMCPServer(BaseMCPServer):
    def __init__(self, github_token: str):
        api_client = BearerTokenAPIClient(
            base_url="https://api.github.com",
            api_token=github_token
        )
        
        super().__init__(
            name="GitHub MCP Server",
            api_client=api_client
        )
    
    def register_tools(self):
        @self.mcp.tool
        @paginated_endpoint()
        async def list_repositories(page: int = 1, per_page: int = 30):
            """List GitHub repositories with automatic pagination."""
            return await self.api_client.get("user/repos", params={
                "page": page,
                "per_page": per_page
            })
        
        @self.mcp.tool
        async def get_repository(owner: str, repo: str):
            """Get detailed repository information."""
            return await self.api_client.get(f"repos/{owner}/{repo}")

# Deploy your server
server = GitHubMCPServer(github_token="your-token")
server.run()  # MCP stdio mode for AI integration
```

### Project Generation Templates

Generate complete MCP server projects instantly:

```
templates/
├── pyproject.toml.template      # Python packaging configuration
├── README.md.template           # Project documentation
├── {{PACKAGE_NAME}}/            # Source code structure
│   ├── __init__.py.template
│   ├── server.py.template       # Main server implementation
│   └── cli.py.template          # Command-line interface
├── tests/                       # Comprehensive test suite
├── .github/workflows/           # GitHub Actions CI/CD
├── Makefile.template            # Development commands
└── .env.example.template        # Environment configuration
```

## Core Components

### Server Foundation
- **`BaseMCPServer`**: Abstract base class providing common MCP server functionality
- **`BaseAPIClient`**: HTTP client with built-in authentication and error handling
- **`BearerTokenAPIClient`**: Industry-standard Bearer token authentication
- **`APIKeyClient`**: API key authentication for simpler services

### Development Utilities
- **`@paginated_endpoint`**: Automatic pagination parameter handling
- **`build_api_params()`**: Clean API parameter dictionary construction
- **`build_search_params()`**: Standardised search endpoint parameters
- **`build_filter_query()`**: Complex API filtering and sorting
- **`MCPToolRegistry`**: Organised tool categorisation and management

## Authentication Strategies

### Bearer Token Authentication (Recommended)
```python
api_client = BearerTokenAPIClient(
    base_url="https://api.service.com/v1",
    api_token="your-bearer-token"
)
```

### API Key Authentication
```python
api_client = APIKeyClient(
    base_url="https://api.service.com/v1",
    api_token="your-api-key",
    api_key_header="X-API-Key"
)
```

### Custom Authentication
```python
class CustomAuthClient(BaseAPIClient):
    def get_auth_headers(self):
        return {"Authorization": f"Custom {self.api_token}"}
```

## Advanced Patterns

### Intelligent Pagination
```python
@self.mcp.tool
@paginated_endpoint(default_per_page=50, max_per_page=200)
async def list_customers(page: int = 1, per_page: int = 50):
    """Automatically handles pagination limits and parameters."""
    params = build_api_params(page=page, per_page=per_page)
    return await self.api_client.get("customers", params=params)
```

### Advanced Filtering
```python
@self.mcp.tool
async def search_projects(
    status: str = None,
    created_after: str = None,
    tags: list = None
):
    """Complex filtering with multiple conditions."""
    conditions = []
    if status:
        conditions.append({"field": "status", "operator": "eq", "value": status})
    
    filter_data = build_filter_query(
        conditions=conditions,
        order_by=[{"field": "created_at", "direction": "desc"}]
    )
    return await self.api_client.post("projects/search", json=filter_data)
```

## Evolution Architecture

MCP Base implements a **shared evolution model** ensuring all servers benefit from library improvements automatically:

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

### Migration Benefits

**Container Support**: When MCP Base adds containerisation, update your import and add a Dockerfile - instant Docker deployment.

**OAuth Integration**: New OAuth support automatically available to all existing servers.

**Performance Improvements**: HTTP client optimisations boost all servers without code changes.

## Real-World Production Usage

MCP Base powers production MCP servers across multiple industries:

- **Capsule CRM**: Complete customer relationship management integration
- **Salesforce**: Enterprise CRM and sales automation  
- **HubSpot**: Marketing and sales platform connectivity
- **GitHub**: Code repository and project management
- **Your API**: Transform any REST API into an AI-accessible service

## Development Workflow

### Local Development
```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run comprehensive tests
pytest

# Code quality checks
make lint

# Start development server
make run-minimal
```

### Project Structure
```bash
your-mcp-server/
├── your_mcp/
│   ├── __init__.py
│   ├── server.py           # Main server logic
│   └── cli.py              # Command-line interface
├── tests/
│   └── test_server.py      # Comprehensive test suite
├── .github/workflows/      # Automated CI/CD
├── pyproject.toml          # Project configuration
├── README.md               # Documentation
└── .env.example            # Environment setup
```

### Quality Assurance
```bash
# Format code automatically
black your_mcp/ tests/
isort your_mcp/ tests/

# Static analysis
ruff check your_mcp/
mypy your_mcp/

# Test coverage
pytest --cov=your_mcp
```

## Deployment

### AI Assistant Integration
```python
server.run()
# Connects directly to AI assistants via stdio protocol
```

### Container Deployment
```dockerfile
FROM python:3.11-slim
COPY . .
RUN pip install -e .
CMD ["your-mcp-server"]
```

## Examples and Learning

### Minimal Implementation
```python
# examples/minimal_server.py
class MinimalMCPServer(BaseMCPServer):
    """Demonstrates basic MCP server in under 20 lines"""
```

### Authentication Showcase  
```python
# examples/auth_patterns.py
# Complete examples of all authentication strategies
BearerTokenAPIClient()    # OAuth 2.0 Bearer tokens
APIKeyClient()           # Simple API key authentication  
CustomAuthClient()       # Custom authentication schemes
```

### Production Patterns
```python
# examples/advanced_patterns.py
@paginated_endpoint()     # Automatic pagination handling
build_filter_query()     # Complex search and filtering
MCPToolRegistry()        # Enterprise tool organisation
```

## Framework Inspiration

MCP Base follows proven patterns from successful frameworks:

- **[FastAPI](https://fastapi.tiangolo.com/)**: Automatic documentation, type safety, performance optimisations
- **[Next.js](https://nextjs.org/)**: Zero-configuration deployment, automatic optimisations, seamless upgrades

These frameworks demonstrate how foundational libraries can evolve while maintaining backward compatibility and automatically improving all dependent projects.

## Technical Architecture

```
┌─────────────────────────────────────┐
│     Your MCP Server Application     │  ← Business logic and API integration
│   (GitHub, Salesforce, Custom)     │
├─────────────────────────────────────┤
│         BaseMCPServer               │  ← MCP protocol implementation
│  • Tool registration               │
│  • HTTP + stdio modes              │  
│  • Authentication middleware       │
├─────────────────────────────────────┤
│        API Client Layer            │  ← HTTP communication
│  • Automatic authentication       │
│  • Error handling & retries       │
│  • Request/response formatting    │
├─────────────────────────────────────┤
│         Utility Functions          │  ← Common patterns
│  • Pagination decorators          │
│  • Parameter builders             │
│  • Environment management         │
└─────────────────────────────────────┘
```

## Community and Contribution

### Contributing Guidelines
1. Fork the repository on GitHub
2. Create a descriptive feature branch
3. Implement changes with comprehensive tests
4. Ensure all quality checks pass
5. Submit a detailed pull request

**Every improvement to MCP Base benefits the entire ecosystem of MCP servers worldwide.**

### Community Projects
- Share your MCP server implementations
- Contribute new authentication strategies
- Suggest API patterns and utilities
- Report issues and enhancement requests

## Support and Documentation

### Resources
- **[Model Context Protocol Specification](https://spec.modelcontextprotocol.io/)**: Official MCP documentation
- **[FastMCP Documentation](https://github.com/jlowin/fastmcp)**: Underlying MCP framework
- **[Project Templates](./templates/)**: Complete project boilerplate
- **[Generation Guide](./CLAUDE.md)**: Detailed development instructions

### Getting Help
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community support and questions
- **Examples**: Working code samples and patterns

## Licence

MIT Licence - see LICENSE file for complete details.

---

**Transform any API into an AI-accessible service with MCP Base - the proven foundation for Model Context Protocol servers.**