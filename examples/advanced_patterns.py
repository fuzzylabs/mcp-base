#!/usr/bin/env python3
"""Advanced patterns and utilities with mcp-base."""

import os
from typing import Dict, Any, Optional, List

from mcp_base import (
    BaseMCPServer, 
    BearerTokenAPIClient, 
    paginated_endpoint,
    build_api_params,
    build_search_params,
    build_filter_query,
    MCPToolRegistry
)


class AdvancedMCPServer(BaseMCPServer):
    """Example showing advanced patterns."""
    
    def __init__(self, api_token: str):
        api_client = BearerTokenAPIClient(
            base_url="https://jsonplaceholder.typicode.com",
            api_token=api_token
        )
        
        super().__init__(
            name="Advanced Patterns Server",
            api_client=api_client,
            auth_required=False
        )
        
        # Optional: Use tool registry for organization
        self.tool_registry = MCPToolRegistry()
    
    def register_tools(self) -> None:
        """Register tools demonstrating advanced patterns."""
        
        # 1. Pagination Pattern
        @self.mcp.tool
        @paginated_endpoint(default_per_page=10, max_per_page=100)
        async def list_posts(
            page: int = 1,
            per_page: int = 10,
            user_id: Optional[int] = None
        ) -> Dict[str, Any]:
            """List posts with pagination.
            
            Args:
                page: Page number (default: 1)
                per_page: Posts per page (default: 10, max: 100)
                user_id: Filter by user ID (optional)
            """
            params = build_api_params(
                page=page,
                per_page=per_page,
                userId=user_id  # API expects userId, not user_id
            )
            
            # Note: JSONPlaceholder doesn't actually support pagination,
            # but this shows the pattern
            posts = await self.api_client.get("posts", params=params)
            
            # Simulate pagination for demo
            start = (page - 1) * per_page
            end = start + per_page
            paginated_posts = posts[start:end] if isinstance(posts, list) else posts
            
            return {
                "posts": paginated_posts,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(posts) if isinstance(posts, list) else 0
                }
            }
        
        # 2. Search Pattern
        @self.mcp.tool
        async def search_posts(
            query: str,
            limit: int = 20
        ) -> Dict[str, Any]:
            """Search posts by title or content.
            
            Args:
                query: Search query
                limit: Maximum results to return
            """
            # Get all posts and filter (real API would handle this server-side)
            posts = await self.api_client.get("posts")
            
            if isinstance(posts, list):
                # Simple text search for demo
                filtered_posts = [
                    post for post in posts
                    if query.lower() in post.get("title", "").lower()
                    or query.lower() in post.get("body", "").lower()
                ][:limit]
            else:
                filtered_posts = []
            
            return {
                "query": query,
                "results": filtered_posts,
                "count": len(filtered_posts)
            }
        
        # 3. Complex Filtering Pattern
        @self.mcp.tool
        async def filter_posts(
            user_ids: Optional[List[int]] = None,
            title_contains: Optional[str] = None,
            min_id: Optional[int] = None
        ) -> Dict[str, Any]:
            """Filter posts with multiple conditions.
            
            Args:
                user_ids: List of user IDs to include
                title_contains: Filter by title content
                min_id: Minimum post ID
            """
            posts = await self.api_client.get("posts")
            
            if not isinstance(posts, list):
                return {"posts": [], "filters_applied": []}
            
            filtered_posts = posts
            filters_applied = []
            
            if user_ids:
                filtered_posts = [p for p in filtered_posts if p.get("userId") in user_ids]
                filters_applied.append(f"user_ids: {user_ids}")
            
            if title_contains:
                filtered_posts = [
                    p for p in filtered_posts 
                    if title_contains.lower() in p.get("title", "").lower()
                ]
                filters_applied.append(f"title_contains: {title_contains}")
            
            if min_id:
                filtered_posts = [p for p in filtered_posts if p.get("id", 0) >= min_id]
                filters_applied.append(f"min_id: {min_id}")
            
            return {
                "posts": filtered_posts,
                "count": len(filtered_posts),
                "filters_applied": filters_applied
            }
        
        # 4. Related Data Pattern
        @self.mcp.tool
        async def get_post_with_comments(post_id: int) -> Dict[str, Any]:
            """Get a post with its comments.
            
            Args:
                post_id: The post ID
            """
            # Make multiple API calls to get related data
            post = await self.api_client.get(f"posts/{post_id}")
            comments = await self.api_client.get(f"posts/{post_id}/comments")
            
            return {
                "post": post,
                "comments": comments,
                "comment_count": len(comments) if isinstance(comments, list) else 0
            }
        
        # 5. Aggregation Pattern
        @self.mcp.tool
        async def get_user_stats(user_id: int) -> Dict[str, Any]:
            """Get aggregated statistics for a user.
            
            Args:
                user_id: The user ID
            """
            # Get user data
            user = await self.api_client.get(f"users/{user_id}")
            
            # Get user's posts
            posts = await self.api_client.get("posts", params={"userId": user_id})
            
            # Get user's albums  
            albums = await self.api_client.get("albums", params={"userId": user_id})
            
            post_count = len(posts) if isinstance(posts, list) else 0
            album_count = len(albums) if isinstance(albums, list) else 0
            
            return {
                "user": user,
                "stats": {
                    "post_count": post_count,
                    "album_count": album_count,
                    "total_content": post_count + album_count
                }
            }
        
        # 6. Error Handling Pattern
        @self.mcp.tool
        async def get_post_safe(post_id: int) -> Dict[str, Any]:
            """Get a post with graceful error handling.
            
            Args:
                post_id: The post ID
            """
            try:
                post = await self.api_client.get(f"posts/{post_id}")
                return {
                    "success": True,
                    "post": post
                }
            except RuntimeError as e:
                return {
                    "success": False,
                    "error": str(e),
                    "post_id": post_id
                }
        
        # Register tools with the registry (optional organization)
        self.tool_registry.register_tool("posts", "list_posts", list_posts)
        self.tool_registry.register_tool("posts", "search_posts", search_posts)
        self.tool_registry.register_tool("posts", "filter_posts", filter_posts)
        self.tool_registry.register_tool("aggregation", "get_user_stats", get_user_stats)


def main():
    """Demo advanced patterns."""
    server = AdvancedMCPServer(api_token="dummy")
    
    print("Advanced Patterns MCP Server")
    print("Demonstrates:")
    print("- Pagination with @paginated_endpoint")
    print("- Search and filtering")
    print("- Related data fetching")
    print("- Aggregation and statistics")
    print("- Error handling patterns")
    print("- Tool organization with registry")
    
    server.run_server()


if __name__ == "__main__":
    main()