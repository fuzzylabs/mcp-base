"""MCP Server Toolkit - A framework for building Model Context Protocol servers."""

from .server import MCPServer
from .base_plugin import BasePlugin

__all__ = ["MCPServer", "BasePlugin"]

__version__ = "0.1.0"