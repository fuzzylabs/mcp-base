"""Tests for the MCPServer class."""

import pytest
from unittest.mock import AsyncMock, MagicMock

from mcp_server_toolkit import MCPServer, BasePlugin


class MockPlugin(BasePlugin):
    """Mock plugin for testing."""
    
    def __init__(self, name: str = "Mock Plugin"):
        super().__init__(name)
        self.initialized = False
        self.cleaned_up = False
        self.tools_registered = False
    
    async def initialize(self) -> None:
        self.initialized = True
    
    async def cleanup(self) -> None:
        self.cleaned_up = True
    
    async def authenticate(self) -> bool:
        return True
    
    def register_tools(self, mcp) -> None:
        self.tools_registered = True


class TestMCPServer:
    """Test cases for MCPServer."""
    
    def test_server_initialization(self):
        """Test server initializes correctly."""
        server = MCPServer(name="Test Server", api_key="test-key")
        assert server.name == "Test Server"
        assert server.api_key == "test-key"
        assert server.auth_required is True
        assert len(server.plugins) == 0
    
    def test_add_plugin(self):
        """Test adding plugins to server."""
        server = MCPServer()
        plugin = MockPlugin()
        
        server.add_plugin(plugin)
        
        assert len(server.plugins) == 1
        assert server.plugins[0] == plugin
    
    @pytest.mark.asyncio
    async def test_initialize_plugins(self):
        """Test plugin initialization."""
        server = MCPServer()
        plugin = MockPlugin()
        server.add_plugin(plugin)
        
        await server.initialize_plugins()
        
        assert plugin.initialized is True
        assert plugin.tools_registered is True
    
    @pytest.mark.asyncio
    async def test_cleanup_plugins(self):
        """Test plugin cleanup."""
        server = MCPServer()
        plugin = MockPlugin()
        server.add_plugin(plugin)
        
        await server.cleanup_plugins()
        
        assert plugin.cleaned_up is True
    
    def test_create_app(self):
        """Test FastAPI app creation."""
        server = MCPServer()
        app = server.create_app()
        
        assert app is not None
        assert server._app == app
        
        # Should return same app on subsequent calls
        app2 = server.create_app()
        assert app == app2