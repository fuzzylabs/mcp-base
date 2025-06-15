"""Utility functions for MCP servers."""

from typing import Any, Dict, List, Optional, Callable
from functools import wraps


def paginated_endpoint(
    default_per_page: int = 50,
    max_per_page: int = 100
) -> Callable:
    """Decorator for paginated API endpoints.
    
    Args:
        default_per_page: Default number of items per page
        max_per_page: Maximum allowed items per page
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Normalize pagination parameters
            page = kwargs.get('page', 1)
            per_page = kwargs.get('per_page', default_per_page)
            
            # Validate pagination parameters
            if page < 1:
                page = 1
            if per_page < 1:
                per_page = default_per_page
            if per_page > max_per_page:
                per_page = max_per_page
            
            kwargs['page'] = page
            kwargs['per_page'] = per_page
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def build_api_params(
    page: Optional[int] = None,
    per_page: Optional[int] = None,
    since: Optional[str] = None,
    archived: Optional[bool] = None,
    **extra_params
) -> Dict[str, Any]:
    """Build API parameters dictionary, excluding None values.
    
    Args:
        page: Page number
        per_page: Items per page
        since: Since date filter
        archived: Include archived items
        **extra_params: Additional parameters
        
    Returns:
        Dictionary of parameters with None values removed
    """
    params = {}
    
    if page is not None:
        params['page'] = page
    if per_page is not None:
        params['perPage'] = per_page
    if since is not None:
        params['since'] = since
    if archived is not None:
        params['archived'] = str(archived).lower()
    
    # Add any extra parameters
    for key, value in extra_params.items():
        if value is not None:
            params[key] = value
    
    return params


def build_search_params(
    keyword: str,
    page: int = 1,
    per_page: int = 50,
    **extra_params
) -> Dict[str, Any]:
    """Build search parameters dictionary.
    
    Args:
        keyword: Search keyword
        page: Page number
        per_page: Items per page
        **extra_params: Additional parameters
        
    Returns:
        Dictionary of search parameters
    """
    params = {
        'q': keyword,
        'page': page,
        'perPage': per_page
    }
    
    # Add any extra parameters
    for key, value in extra_params.items():
        if value is not None:
            params[key] = value
    
    return params


def build_filter_query(
    conditions: List[Dict[str, str]],
    order_by: Optional[List[Dict[str, str]]] = None,
    page: int = 1,
    per_page: int = 50
) -> Dict[str, Any]:
    """Build a filter query for advanced API filtering.
    
    Args:
        conditions: List of filter conditions
        order_by: List of sorting specifications
        page: Page number
        per_page: Items per page
        
    Returns:
        Dictionary formatted for filter API endpoints
    """
    filter_data = {
        "filter": {
            "conditions": conditions,
        },
        "page": page,
        "perPage": per_page,
    }
    
    if order_by:
        filter_data["filter"]["orderBy"] = order_by
    
    return filter_data


class MCPToolRegistry:
    """Registry for organizing MCP tools by category."""
    
    def __init__(self):
        self.tools = {}
        self.categories = {}
    
    def register_tool(self, category: str, tool_name: str, tool_func: Callable):
        """Register a tool in a specific category.
        
        Args:
            category: Tool category (e.g., 'contacts', 'opportunities')
            tool_name: Name of the tool
            tool_func: The tool function
        """
        if category not in self.categories:
            self.categories[category] = []
        
        self.categories[category].append(tool_name)
        self.tools[tool_name] = {
            'category': category,
            'function': tool_func
        }
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get all tool names in a category.
        
        Args:
            category: The category name
            
        Returns:
            List of tool names in the category
        """
        return self.categories.get(category, [])
    
    def get_all_categories(self) -> List[str]:
        """Get all category names.
        
        Returns:
            List of all category names
        """
        return list(self.categories.keys())


def require_env_var(var_name: str, default_for_tests: Optional[str] = None) -> str:
    """Require an environment variable with optional test default.
    
    Args:
        var_name: Name of the environment variable
        default_for_tests: Default value to use during tests
        
    Returns:
        The environment variable value
        
    Raises:
        RuntimeError: If the environment variable is not set
    """
    import os
    
    value = os.getenv(var_name)
    
    if not value and os.getenv("PYTEST_CURRENT_TEST") and default_for_tests:
        return default_for_tests
    
    if not value:
        raise RuntimeError(
            f"{var_name} environment variable is required. "
            f"Please set it and restart the server."
        )
    
    return value