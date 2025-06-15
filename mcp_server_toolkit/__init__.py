"""MCP Server Toolkit - A library for building Model Context Protocol servers."""

from .server import BaseMCPServer
from .api_client import BaseAPIClient, BearerTokenAPIClient, APIKeyClient
from .capsule_server import CapsuleMCPServer
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
    "CapsuleMCPServer",
    "paginated_endpoint",
    "build_api_params",
    "build_search_params",
    "build_filter_query",
    "MCPToolRegistry",
    "require_env_var",
]

__version__ = "0.1.0"