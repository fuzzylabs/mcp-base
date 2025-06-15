#!/usr/bin/env python3
"""Minimal example of an MCP server using mcp-base."""

import os
from typing import Dict, Any

from mcp_base import BaseMCPServer, BearerTokenAPIClient


class MinimalMCPServer(BaseMCPServer):
    """A minimal MCP server example."""
    
    def __init__(self, api_token: str, mcp_api_key: str = None):
        # Create a simple API client
        api_client = BearerTokenAPIClient(
            base_url="https://jsonplaceholder.typicode.com",
            api_token=api_token,
            user_agent="minimal-mcp-server/1.0"
        )
        
        super().__init__(
            name="Minimal MCP Server",
            api_client=api_client,
            mcp_api_key=mcp_api_key,
            auth_required=False,  # Disable auth for example
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
    server = MinimalMCPServer(
        api_token="dummy-token",  # JSONPlaceholder doesn't need real auth
        mcp_api_key=os.getenv("MCP_API_KEY")
    )
    
    print("Starting Minimal MCP Server on http://localhost:8000")
    print("Try: curl http://localhost:8000/health")
    server.run_server()


if __name__ == "__main__":
    main()