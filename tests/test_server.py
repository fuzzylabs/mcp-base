"""Tests for the MCP Server classes."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from typing import Dict, Any

from mcp_base import BaseMCPServer, BaseAPIClient


class MockAPIClient(BaseAPIClient):
    """Mock API client for testing."""
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get mock auth headers."""
        return {"Authorization": "Bearer test-token"}
    
    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Mock request method."""
        return {"status": "ok", "method": method, "endpoint": endpoint}


class MockMCPServer(BaseMCPServer):
    """Mock MCP server for testing."""
    
    def register_tools(self) -> None:
        """Register mock tools."""
        @self.mcp.tool
        async def test_tool() -> Dict[str, Any]:
            """Test tool."""
            return {"result": "test"}


class TestBaseMCPServer:
    """Test cases for BaseMCPServer."""
    
    def test_server_initialization(self):
        """Test server initializes correctly."""
        api_client = MockAPIClient("https://api.example.com", "test-token")
        server = MockMCPServer(
            name="Test Server",
            api_client=api_client,
        )
        
        assert server.name == "Test Server"
        assert server.api_client == api_client
    
    @pytest.mark.asyncio
    async def test_connection_test(self):
        """Test connection testing."""
        api_client = MockAPIClient("https://api.example.com", "test-token")
        server = MockMCPServer(
            name="Test Server",
            api_client=api_client
        )
        
        # Should return True by default
        result = await server.test_connection()
        assert result is True
    
    def test_tools_registration(self):
        """Test that tools are registered."""
        server = MockMCPServer(name="Test Server")
        
        # Should have MCP instance with tools
        assert server.mcp is not None


class TestBaseAPIClient:
    """Test cases for BaseAPIClient."""
    
    def test_client_initialization(self):
        """Test API client initializes correctly."""
        client = MockAPIClient("https://api.example.com", "test-token")
        
        assert client.base_url == "https://api.example.com"
        assert client.api_token == "test-token"
        assert client.timeout == 20
    
    def test_get_default_headers(self):
        """Test default headers."""
        client = MockAPIClient("https://api.example.com", "test-token")
        headers = client.get_default_headers()
        
        assert "Accept" in headers
        assert "Content-Type" in headers
        assert "User-Agent" in headers
        assert "Authorization" in headers
    
    @pytest.mark.asyncio
    async def test_convenience_methods(self):
        """Test convenience HTTP methods."""
        client = MockAPIClient("https://api.example.com", "test-token")
        
        # Test GET
        result = await client.get("test")
        assert result["method"] == "GET"
        assert result["endpoint"] == "test"
        
        # Test POST
        result = await client.post("test")
        assert result["method"] == "POST"