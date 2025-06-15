#!/usr/bin/env python3
"""Examples of different authentication patterns with mcp-base."""

import os
from typing import Dict, Any

from mcp_base import BaseMCPServer, BearerTokenAPIClient, APIKeyClient, BaseAPIClient


class CustomAuthClient(BaseAPIClient):
    """Example of custom authentication."""
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Custom auth headers (e.g., for services using custom schemes)."""
        if not self.api_token:
            return {}
        return {
            "X-Custom-Auth": f"CustomScheme {self.api_token}",
            "X-Client-Version": "1.0"
        }


class BearerTokenServer(BaseMCPServer):
    """Example using Bearer token authentication."""
    
    def __init__(self, api_token: str):
        api_client = BearerTokenAPIClient(
            base_url="https://api.example.com/v1",
            api_token=api_token
        )
        
        super().__init__(
            name="Bearer Token Server",
            api_client=api_client,
        )
    
    def register_tools(self):
        @self.mcp.tool
        async def bearer_example() -> Dict[str, Any]:
            """Example tool using Bearer token auth."""
            return await self.api_client.get("protected-endpoint")


class APIKeyServer(BaseMCPServer):
    """Example using API key authentication."""
    
    def __init__(self, api_key: str):
        api_client = APIKeyClient(
            base_url="https://api.example.com/v1",
            api_token=api_key,
            api_key_header="X-API-Key"  # Custom header name
        )
        
        super().__init__(
            name="API Key Server",
            api_client=api_client,
        )
    
    def register_tools(self):
        @self.mcp.tool
        async def api_key_example() -> Dict[str, Any]:
            """Example tool using API key auth."""
            return await self.api_client.get("data")


class CustomAuthServer(BaseMCPServer):
    """Example using custom authentication."""
    
    def __init__(self, api_token: str):
        api_client = CustomAuthClient(
            base_url="https://api.custom.com/v1",
            api_token=api_token
        )
        
        super().__init__(
            name="Custom Auth Server",
            api_client=api_client,
        )
    
    def register_tools(self):
        @self.mcp.tool
        async def custom_auth_example() -> Dict[str, Any]:
            """Example tool using custom auth."""
            return await self.api_client.get("custom-endpoint")


class NoAuthServer(BaseMCPServer):
    """Example for public APIs that don't require authentication."""
    
    def __init__(self):
        # No API client needed for this example
        super().__init__(
            name="No Auth Server",
            api_client=None,
        )
    
    def register_tools(self):
        @self.mcp.tool
        async def public_data() -> Dict[str, Any]:
            """Example tool for public data."""
            # You could use httpx directly or create a simple client
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get("https://jsonplaceholder.typicode.com/posts/1")
                return response.json()


def main():
    """Demo different auth patterns."""
    print("Authentication Patterns Examples:")
    print("1. Bearer Token - Most common for REST APIs")
    print("2. API Key - Common for simple APIs") 
    print("3. Custom Auth - For non-standard authentication")
    print("4. No Auth - For public APIs")
    
    # Example: Bearer token server
    # server = BearerTokenServer(api_token="your-bearer-token")
    # server.run_server()


if __name__ == "__main__":
    main()