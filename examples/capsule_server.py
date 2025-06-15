#!/usr/bin/env python3
"""Example Capsule CRM MCP Server using the toolkit."""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the toolkit
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server_toolkit import MCPServer
from mcp_server_toolkit.plugins import CapsulePlugin


def main():
    """Main entry point for the Capsule CRM MCP server."""
    # Create the server
    server = MCPServer(
        name="Capsule CRM MCP Server",
        api_key=os.getenv("MCP_API_KEY"),
        auth_required=True,
    )
    
    # Create and add the Capsule plugin
    capsule_plugin = CapsulePlugin(config={
        "base_url": os.getenv("CAPSULE_BASE_URL", "https://api.capsulecrm.com/api/v2"),
        "api_token": os.getenv("CAPSULE_API_TOKEN"),
    })
    server.add_plugin(capsule_plugin)
    
    # Check if we should run in stdio mode (for MCP clients)
    if len(sys.argv) > 1 and sys.argv[1] == "stdio":
        server.run_stdio()
    else:
        # Run as HTTP server
        print("Starting Capsule CRM MCP Server on http://localhost:8000")
        print("Use /health endpoint to check server status")
        print("MCP endpoints available at /mcp/")
        server.run_server(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()