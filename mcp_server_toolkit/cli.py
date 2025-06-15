"""Command-line interface for MCP Server Toolkit."""

import argparse
import os
import sys
from typing import Dict, Any

from .server import MCPServer
from .plugins import CapsulePlugin


def create_capsule_server() -> MCPServer:
    """Create a Capsule CRM MCP server."""
    server = MCPServer(
        name="Capsule CRM MCP Server",
        api_key=os.getenv("MCP_API_KEY"),
        auth_required=True,
    )
    
    capsule_plugin = CapsulePlugin(config={
        "base_url": os.getenv("CAPSULE_BASE_URL", "https://api.capsulecrm.com/api/v2"),
        "api_token": os.getenv("CAPSULE_API_TOKEN"),
    })
    server.add_plugin(capsule_plugin)
    
    return server


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="MCP Server Toolkit")
    parser.add_argument(
        "server_type",
        choices=["capsule"],
        help="Type of MCP server to run",
    )
    parser.add_argument(
        "mode",
        choices=["http", "stdio"],
        help="Server mode: http for web server, stdio for MCP client",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind to (http mode only)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (http mode only)",
    )
    
    args = parser.parse_args()
    
    # Create the appropriate server
    if args.server_type == "capsule":
        server = create_capsule_server()
    else:
        print(f"Unknown server type: {args.server_type}")
        sys.exit(1)
    
    # Run the server
    if args.mode == "stdio":
        server.run_stdio()
    else:
        print(f"Starting {server.name} on http://{args.host}:{args.port}")
        print("Use /health endpoint to check server status")
        print("MCP endpoints available at /mcp/")
        server.run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()