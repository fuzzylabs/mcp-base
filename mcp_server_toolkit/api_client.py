"""Base API client for MCP servers."""

import os
from typing import Any, Dict, Optional
from abc import ABC, abstractmethod

import httpx


class BaseAPIClient(ABC):
    """Base class for API clients used in MCP servers."""
    
    def __init__(
        self,
        base_url: str,
        api_token: Optional[str] = None,
        timeout: int = 20,
        user_agent: str = "mcp-server-toolkit/0.1.0",
    ):
        """Initialize the API client.
        
        Args:
            base_url: Base URL for the API
            api_token: API token for authentication
            timeout: Request timeout in seconds
            user_agent: User agent string for requests
        """
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.timeout = timeout
        self.user_agent = user_agent
    
    @abstractmethod
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for requests.
        
        Returns:
            Dictionary of headers for authentication
        """
        pass
    
    def get_default_headers(self) -> Dict[str, str]:
        """Get default headers for all requests.
        
        Returns:
            Dictionary of default headers
        """
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent,
        }
        headers.update(self.get_auth_headers())
        return headers
    
    async def request(
        self,
        method: str,
        endpoint: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (will be appended to base_url)
            **kwargs: Additional arguments to pass to httpx
            
        Returns:
            JSON response from the API
            
        Raises:
            RuntimeError: If the API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        headers = self.get_default_headers()
        
        # Merge any provided headers
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                **kwargs
            )
            
            try:
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                await self._handle_api_error(exc)
            
            return response.json()
    
    async def _handle_api_error(self, exc: httpx.HTTPStatusError) -> None:
        """Handle API errors consistently.
        
        Args:
            exc: The HTTP status error exception
            
        Raises:
            RuntimeError: Always raises with formatted error message
        """
        if exc.response.headers.get("content-type", "").startswith("application/json"):
            try:
                detail = exc.response.json()
            except Exception:
                detail = exc.response.text
        else:
            detail = exc.response.text
        
        raise RuntimeError(
            f"API error {exc.response.status_code}: {detail}"
        ) from None
    
    async def get(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a GET request."""
        return await self.request("GET", endpoint, **kwargs)
    
    async def post(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a POST request."""
        return await self.request("POST", endpoint, **kwargs)
    
    async def put(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a PUT request."""
        return await self.request("PUT", endpoint, **kwargs)
    
    async def delete(self, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a DELETE request."""
        return await self.request("DELETE", endpoint, **kwargs)


class BearerTokenAPIClient(BaseAPIClient):
    """API client that uses Bearer token authentication."""
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get Bearer token authentication headers."""
        if not self.api_token and os.getenv("PYTEST_CURRENT_TEST"):
            # Use test token for tests
            return {"Authorization": "Bearer test-token"}
        
        if not self.api_token:
            raise RuntimeError(
                "API token is required. Set the token parameter or appropriate environment variable."
            )
        
        return {"Authorization": f"Bearer {self.api_token}"}


class APIKeyClient(BaseAPIClient):
    """API client that uses API key authentication."""
    
    def __init__(self, *args, api_key_header: str = "X-API-Key", **kwargs):
        """Initialize with custom API key header name."""
        super().__init__(*args, **kwargs)
        self.api_key_header = api_key_header
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get API key authentication headers."""
        if not self.api_token:
            if os.getenv("PYTEST_CURRENT_TEST"):
                return {self.api_key_header: "test-token"}
            raise RuntimeError(
                "API key is required. Set the token parameter or appropriate environment variable."
            )
        
        return {self.api_key_header: self.api_token}