"""Base plugin interface for MCP Server Toolkit."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from fastmcp import FastMCP


class BasePlugin(ABC):
    """Base class for all MCP server plugins."""
    
    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize the plugin with a name and configuration.
        
        Args:
            name: The name of the plugin
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.tools: List[Callable] = []
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin. Called when the server starts."""
        pass
    
    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup plugin resources. Called when the server shuts down."""
        pass
    
    @abstractmethod
    def register_tools(self, mcp: FastMCP) -> None:
        """Register the plugin's tools with the MCP server.
        
        Args:
            mcp: The FastMCP server instance to register tools with
        """
        pass
    
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the external service.
        
        Returns:
            True if authentication successful, False otherwise
        """
        pass
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get a configuration value for this plugin.
        
        Args:
            key: The configuration key
            default: Default value if key not found
            
        Returns:
            The configuration value
        """
        return self.config.get(key, default)
    
    def validate_required_config(self, required_keys: List[str]) -> None:
        """Validate that required configuration keys are present.
        
        Args:
            required_keys: List of required configuration keys
            
        Raises:
            ValueError: If any required key is missing
        """
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            raise ValueError(f"Missing required configuration keys for {self.name}: {missing_keys}")