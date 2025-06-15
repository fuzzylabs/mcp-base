#!/usr/bin/env python3
"""Example of building a custom MCP server using the toolkit."""

import os
import sys
from pathlib import Path
from typing import Any, Dict

# Add the parent directory to the path so we can import the toolkit
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server_toolkit import (
    BaseMCPServer,
    BaseAPIClient,
    paginated_endpoint,
    build_api_params,
)


class CustomAPIClient(BaseAPIClient):
    """Example custom API client."""
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers."""
        if not self.api_token:
            return {}
        return {"Authorization": f"Bearer {self.api_token}"}


class CustomMCPServer(BaseMCPServer):
    """Example custom MCP server."""
    
    def __init__(self, api_token: str = None, mcp_api_key: str = None):
        # Create API client
        api_client = CustomAPIClient(
            base_url="https://api.example.com/v1",
            api_token=api_token or os.getenv("CUSTOM_API_TOKEN"),
        )
        
        super().__init__(
            name="Custom MCP Server",
            api_client=api_client,
            mcp_api_key=mcp_api_key,
            auth_required=True,
        )
    
    async def test_connection(self) -> bool:
        """Test connection to the API."""
        try:
            # Replace with actual API endpoint
            await self.api_client.get("ping")
            return True
        except Exception:
            return False
    
    def register_tools(self) -> None:
        """Register tools with the MCP server."""
        
        @self.mcp.tool
        @paginated_endpoint()
        async def list_items(
            page: int = 1,
            per_page: int = 50,
            category: str = None,
        ) -> Dict[str, Any]:
            \"\"\"List items from the API.
            
            Args:
                page: Page number
                per_page: Items per page
                category: Optional category filter
            \"\"\"
            params = build_api_params(
                page=page,
                per_page=per_page,
                category=category
            )
            return await self.api_client.get("items", params=params)
        
        @self.mcp.tool
        async def get_item(item_id: int) -> Dict[str, Any]:
            \"\"\"Get a specific item by ID.\"\"\"
            return await self.api_client.get(f"items/{item_id}")
        
        @self.mcp.tool
        async def search_items(query: str) -> Dict[str, Any]:
            \"\"\"Search for items.\"\"\"
            return await self.api_client.get("items/search", params={"q": query})


def main():
    """Main entry point."""
    server = CustomMCPServer(
        api_token=os.getenv("CUSTOM_API_TOKEN"),
        mcp_api_key=os.getenv("MCP_API_KEY"),
    )
    
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        server.run_stdio()
    else:
        print("Starting Custom MCP Server on http://localhost:8000")
        server.run_server(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()