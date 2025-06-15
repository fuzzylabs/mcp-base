"""Base MCP Server classes and utilities."""

import os
from typing import Any, Dict, Optional
from contextlib import asynccontextmanager
from abc import ABC, abstractmethod

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse
from fastmcp import FastMCP

from .api_client import BaseAPIClient


class BaseMCPServer(ABC):
    """Base class for MCP servers with common functionality."""
    
    def __init__(
        self,
        name: str,
        api_client: Optional[BaseAPIClient] = None,
        mcp_api_key: Optional[str] = None,
        auth_required: bool = True,
    ):
        """Initialize the MCP Server.
        
        Args:
            name: Name of the MCP server
            api_client: API client for external service
            mcp_api_key: API key for MCP authentication (can also be set via MCP_API_KEY env var)
            auth_required: Whether MCP authentication is required
        """
        self.name = name
        self.api_client = api_client
        self.mcp_api_key = mcp_api_key or os.getenv("MCP_API_KEY")
        self.auth_required = auth_required and self.mcp_api_key is not None
        
        # Create the MCP instance
        self.mcp = FastMCP(
            name=self.name,
            auth=None,
            json_response=True,
            stateless_http=True,
        )
        
        self._app: Optional[FastAPI] = None
        
        # Register tools during initialization
        self.register_tools()
    
    @abstractmethod
    def register_tools(self) -> None:
        """Register MCP tools. Must be implemented by subclasses."""
        pass
    
    async def initialize(self) -> None:
        """Initialize the server. Override in subclasses if needed."""
        if self.api_client:
            # Test API client connection if available
            await self.test_connection()
    
    async def cleanup(self) -> None:
        """Cleanup server resources. Override in subclasses if needed."""
        pass
    
    async def test_connection(self) -> bool:
        """Test connection to external API. Override in subclasses."""
        return True
    
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
        if provided_key != self.mcp_api_key:
            raise HTTPException(status_code=401, detail="Invalid API key")
    
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        """Lifespan context manager for FastAPI app."""
        # Startup
        await self.initialize()
        yield
        # Shutdown
        await self.cleanup()
    
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
            return {
                "status": "healthy",
                "server": self.name,
                "has_api_client": self.api_client is not None
            }
        
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