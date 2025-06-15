"""MCP Base - A foundational library for building Model Context Protocol servers."""

from .server import BaseMCPServer
from .api_client import BaseAPIClient, BearerTokenAPIClient, APIKeyClient
from .utils import (
    paginated_endpoint,
    build_api_params,
    build_search_params,
    build_filter_query,
    MCPToolRegistry,
    require_env_var,
)

__all__ = [
    "BaseMCPServer",
    "BaseAPIClient",
    "BearerTokenAPIClient", 
    "APIKeyClient",
    "paginated_endpoint",
    "build_api_params",
    "build_search_params",
    "build_filter_query",
    "MCPToolRegistry",
    "require_env_var",
]

__version__ = "0.1.0"