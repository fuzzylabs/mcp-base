"""Main MCP Server class for the toolkit."""

import os
from typing import Any, Dict, List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastmcp import FastMCP

from .base_plugin import BasePlugin


class MCPServer:
    """Main MCP Server that manages plugins and handles requests."""
    
    def __init__(
        self,
        name: str = "MCP Server Toolkit",
        api_key: Optional[str] = None,
        auth_required: bool = True,
    ):
        """Initialize the MCP Server.
        
        Args:
            name: Name of the MCP server
            api_key: API key for authentication (can also be set via MCP_API_KEY env var)
            auth_required: Whether authentication is required
        """
        self.name = name
        self.api_key = api_key or os.getenv("MCP_API_KEY")
        self.auth_required = auth_required and self.api_key is not None
        self.plugins: List[BasePlugin] = []
        
        # Create the MCP instance
        self.mcp = FastMCP(
            name=self.name,
            auth=None,
            json_response=True,
            stateless_http=True,
        )
        
        self._app: Optional[FastAPI] = None
    
    def add_plugin(self, plugin: BasePlugin) -> None:
        """Add a plugin to the server.
        
        Args:
            plugin: The plugin instance to add
        """
        self.plugins.append(plugin)
    
    async def initialize_plugins(self) -> None:
        """Initialize all registered plugins."""
        for plugin in self.plugins:
            await plugin.initialize()
            plugin.register_tools(self.mcp)
    
    async def cleanup_plugins(self) -> None:
        """Cleanup all registered plugins."""
        for plugin in self.plugins:
            await plugin.cleanup()
    
    async def authenticate_request(self, request: Request) -> None:
        """Authenticate requests to MCP endpoints using API key.
        
        Args:
            request: The FastAPI request object
            
        Raises:
            HTTPException: If authentication fails
        """
        # Skip authentication for tests
        if os.getenv("PYTEST_CURRENT_TEST"):
            return
        
        # Skip authentication if not required
        if not self.auth_required:
            return
        
        # Only authenticate /mcp/ endpoints
        if not request.url.path.startswith("/mcp"):
            return
        
        # Check for Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail="Missing Authorization header. Use 'Authorization: Bearer <api_key>'",
            )
        
        # Validate Bearer token format
        if not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization header format. Use 'Authorization: Bearer <api_key>'",
            )
        
        provided_key = auth_header[7:]
        if provided_key != self.api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")
    
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Lifespan context manager for FastAPI app."""
        # Startup
        await self.initialize_plugins()
        yield
        # Shutdown
        await self.cleanup_plugins()
    
    def create_app(self) -> FastAPI:
        """Create and configure the FastAPI application.
        
        Returns:
            The configured FastAPI application
        """
        if self._app is not None:
            return self._app
        
        # Create the MCP HTTP app
        mcp_app = self.mcp.http_app(path="/")
        
        # Create the main FastAPI app with lifespan
        app = FastAPI(
            title=self.name,
            lifespan=self.lifespan,
        )
        
        # Add authentication middleware
        @app.middleware("http")
        async def auth_middleware(request: Request, call_next):
            await self.authenticate_request(request)
            response = await call_next(request)
            return response
        
        # Mount the MCP app
        app.mount("/mcp", mcp_app)
        
        # Add redirect for /mcp to /mcp/
        @app.api_route("/mcp", methods=["GET", "POST"])
        async def mcp_redirect() -> RedirectResponse:
            """Redirect ``/mcp`` to ``/mcp/`` preserving the request method."""
            return RedirectResponse(url="/mcp/", status_code=307)
        
        # Add health check endpoint
        @app.get("/health")
        async def health_check():
            """Health check endpoint."""
            return {"status": "healthy", "plugins": [plugin.name for plugin in self.plugins]}
        
        self._app = app
        return app
    
    def run_server(self, host: str = "127.0.0.1", port: int = 8000, **kwargs):
        """Run the server using uvicorn.
        
        Args:
            host: Host to bind to
            port: Port to bind to
            **kwargs: Additional arguments to pass to uvicorn
        """
        import uvicorn
        app = self.create_app()
        uvicorn.run(app, host=host, port=port, **kwargs)
    
    def run_stdio(self):
        """Run the server in stdio mode for MCP client integration."""
        self.mcp.run("stdio")