#!/usr/bin/env python3
"""Minimal example of an MCP server using mcp-base."""

import os
from typing import Dict, Any

from mcp_base import BaseMCPServer, BearerTokenAPIClient


class MinimalMCPServer(BaseMCPServer):
    """A minimal MCP server example."""
    
    def __init__(self, api_token: str):
        # Create a simple API client
        api_client = BearerTokenAPIClient(
            base_url="https://jsonplaceholder.typicode.com",
            api_token=api_token,
            user_agent="minimal-mcp-server/1.0"
        )
        
        super().__init__(
            name="Minimal MCP Server",
            api_client=api_client,
        )
    
    async def test_connection(self) -> bool:
        """Test connection to the API."""
        try:
            await self.api_client.get("posts/1")
            return True
        except Exception:
            return False
    
    def register_tools(self) -> None:
        """Register MCP tools."""
        
        @self.mcp.tool
        async def get_post(post_id: int) -> Dict[str, Any]:
            """Get a blog post by ID.
            
            Args:
                post_id: The ID of the post to retrieve
            """
            return await self.api_client.get(f"posts/{post_id}")
        
        @self.mcp.tool
        async def list_posts() -> Dict[str, Any]:
            """List all blog posts."""
            posts = await self.api_client.get("posts")
            return {"posts": posts}


def main():
    """Run the minimal server."""
    server = MinimalMCPServer(api_token="dummy-token")  # JSONPlaceholder doesn't need real auth
    
    print("Starting Minimal MCP Server in stdio mode")
    print("Connect via MCP client")
    server.run()


if __name__ == "__main__":
    main()