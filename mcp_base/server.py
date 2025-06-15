"""Base MCP Server classes and utilities."""

import os
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

from fastmcp import FastMCP

from .api_client import BaseAPIClient


class BaseMCPServer(ABC):
    """Base class for MCP servers with common functionality."""
    
    def __init__(
        self,
        name: str,
        api_client: Optional[BaseAPIClient] = None,
    ):
        """Initialize the MCP Server.
        
        Args:
            name: Name of the MCP server
            api_client: API client for external service
        """
        self.name = name
        self.api_client = api_client
        
        # Create the MCP instance
        self.mcp = FastMCP(name=self.name)
        
        # Register tools during initialization
        self.register_tools()
    
    @abstractmethod
    def register_tools(self) -> None:
        """Register MCP tools. Must be implemented by subclasses."""
        pass
    
    async def test_connection(self) -> bool:
        """Test connection to external API. Override in subclasses."""
        return True
    
    def run(self):
        """Run the MCP server in stdio mode."""
        self.mcp.run("stdio")