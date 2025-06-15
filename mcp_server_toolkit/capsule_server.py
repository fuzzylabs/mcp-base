"""Capsule CRM MCP Server using the toolkit."""

import os
from typing import Any, Dict, Optional

from .server import BaseMCPServer
from .api_client import BearerTokenAPIClient
from .utils import build_api_params, build_search_params, build_filter_query, paginated_endpoint


class CapsuleMCPServer(BaseMCPServer):
    """MCP Server for Capsule CRM integration."""
    
    def __init__(
        self,
        base_url: str = "https://api.capsulecrm.com/api/v2",
        api_token: Optional[str] = None,
        mcp_api_key: Optional[str] = None,
        auth_required: bool = True,
    ):
        """Initialize the Capsule MCP Server.
        
        Args:
            base_url: Capsule API base URL
            api_token: Capsule API token (can also be set via CAPSULE_API_TOKEN env var)
            mcp_api_key: API key for MCP authentication
            auth_required: Whether MCP authentication is required
        """
        # Get API token from environment if not provided
        api_token = api_token or os.getenv("CAPSULE_API_TOKEN")
        
        # Create API client
        api_client = BearerTokenAPIClient(
            base_url=base_url,
            api_token=api_token,
            user_agent="mcp-server-toolkit/0.1.0 (+https://github.com/fuzzylabs/mcp-server-toolkit)"
        )
        
        super().__init__(
            name="Capsule CRM MCP Server",
            api_client=api_client,
            mcp_api_key=mcp_api_key,
            auth_required=auth_required,
        )
    
    async def test_connection(self) -> bool:
        """Test connection to Capsule API."""
        try:
            # Test with a simple API call
            await self.api_client.get("users", params={"perPage": 1})
            return True
        except Exception:
            return False
    
    def register_tools(self) -> None:
        """Register all Capsule CRM tools with the MCP server."""
        
        # Contact tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_contacts(
            page: int = 1,
            per_page: int = 50,
            archived: bool = False,
            since: str = None,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of contacts.

            Args:
                page: Page number (default: 1)
                per_page: Number of contacts per page (default: 50, max: 100)
                archived: Include archived contacts (default: false)
                since: Only return contacts modified since this date (ISO8601 format, e.g. '2024-01-01T00:00:00Z')
            \"\"\"
            params = build_api_params(page=page, per_page=per_page, archived=archived, since=since)
            return await self.api_client.get("parties", params=params)

        @self.mcp.tool
        @paginated_endpoint()
        async def search_contacts(
            keyword: str,
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Fuzzy search contacts by name, email, or organisation.\"\"\"
            params = build_search_params(keyword, page, per_page)
            return await self.api_client.get("parties/search", params=params)

        @self.mcp.tool
        @paginated_endpoint()
        async def list_recent_contacts(
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Return contacts sorted by most recently contacted/updated.\"\"\"
            filter_data = build_filter_query(
                conditions=[{"field": "type", "operator": "is", "value": "person"}],
                order_by=[{"field": "lastContactedOn", "direction": "descending"}],
                page=page,
                per_page=per_page
            )
            return await self.api_client.post("parties/filters/results", json=filter_data)

        @self.mcp.tool
        async def get_contact(contact_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific contact.\"\"\"
            return await self.api_client.get(f"parties/{contact_id}")

        # Opportunity tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_opportunities(
            page: int = 1,
            per_page: int = 50,
            since: str = None,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of opportunities.

            Args:
                page: Page number (default: 1)
                per_page: Number of opportunities per page (default: 50, max: 100)
                since: Only return opportunities modified since this date (ISO8601 format, e.g. '2024-01-01T00:00:00Z')
            \"\"\"
            params = build_api_params(page=page, per_page=per_page, since=since)
            return await self.api_client.get("opportunities", params=params)

        @self.mcp.tool
        @paginated_endpoint()
        async def list_open_opportunities(
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Return open opportunities using filters API for proper filtering and sorting.\"\"\"
            filter_data = build_filter_query(
                conditions=[
                    {"field": "milestone", "operator": "is not", "value": "won"},
                    {"field": "milestone", "operator": "is not", "value": "lost"},
                ],
                order_by=[{"field": "expectedCloseOn", "direction": "ascending"}],
                page=page,
                per_page=per_page
            )
            return await self.api_client.post("opportunities/filters/results", json=filter_data)

        @self.mcp.tool
        async def get_opportunity(opportunity_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific opportunity.\"\"\"
            return await self.api_client.get(f"opportunities/{opportunity_id}")

        # Case tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_cases(
            page: int = 1,
            per_page: int = 50,
            since: str = None,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of support cases.

            Args:
                page: Page number (default: 1)
                per_page: Number of cases per page (default: 50, max: 100)
                since: Only return cases modified since this date (ISO8601 format)
            \"\"\"
            params = build_api_params(page=page, per_page=per_page, since=since)
            return await self.api_client.get("kases", params=params)

        @self.mcp.tool
        @paginated_endpoint()
        async def search_cases(
            keyword: str,
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Search support cases by keyword.\"\"\"
            params = build_search_params(keyword, page, per_page)
            return await self.api_client.get("kases/search", params=params)

        @self.mcp.tool
        async def get_case(case_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific support case.\"\"\"
            return await self.api_client.get(f"kases/{case_id}")

        # Task tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_tasks(
            page: int = 1,
            per_page: int = 50,
            since: str = None,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of tasks.

            Args:
                page: Page number (default: 1)
                per_page: Number of tasks per page (default: 50, max: 100)
                since: Only return tasks modified since this date (ISO8601 format)
            \"\"\"
            params = build_api_params(page=page, per_page=per_page, since=since)
            return await self.api_client.get("tasks", params=params)

        @self.mcp.tool
        async def get_task(task_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific task.\"\"\"
            return await self.api_client.get(f"tasks/{task_id}")

        # Timeline entry tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_entries(
            page: int = 1,
            per_page: int = 50,
            since: str = None,
        ) -> Dict[str, Any]:
            \"\"\"Return timeline entries (notes, emails, calls, etc.).

            Args:
                page: Page number (default: 1)
                per_page: Number of entries per page (default: 50, max: 100)
                since: Only return entries modified since this date (ISO8601 format)
            \"\"\"
            params = build_api_params(page=page, per_page=per_page, since=since)
            return await self.api_client.get("entries", params=params)

        @self.mcp.tool
        async def get_entry(entry_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific timeline entry.\"\"\"
            return await self.api_client.get(f"entries/{entry_id}")

        # Project tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_projects(
            page: int = 1,
            per_page: int = 50,
            since: str = None,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of projects.

            Args:
                page: Page number (default: 1)
                per_page: Number of projects per page (default: 50, max: 100)
                since: Only return projects modified since this date (ISO8601 format)
            \"\"\"
            params = build_api_params(page=page, per_page=per_page, since=since)
            return await self.api_client.get("projects", params=params)

        @self.mcp.tool
        async def get_project(project_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific project.\"\"\"
            return await self.api_client.get(f"projects/{project_id}")

        # Tag tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_tags(
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of tags.\"\"\"
            params = build_api_params(page=page, per_page=per_page)
            return await self.api_client.get("tags", params=params)

        @self.mcp.tool
        async def get_tag(tag_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific tag.\"\"\"
            return await self.api_client.get(f"tags/{tag_id}")

        # User tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_users(
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of users.\"\"\"
            params = build_api_params(page=page, per_page=per_page)
            return await self.api_client.get("users", params=params)

        @self.mcp.tool
        async def get_user(user_id: int) -> Dict[str, Any]:
            \"\"\"Get detailed information about a specific user.\"\"\"
            return await self.api_client.get(f"users/{user_id}")

        # Configuration tools
        @self.mcp.tool
        async def list_pipelines() -> Dict[str, Any]:
            \"\"\"Return a list of sales pipelines.\"\"\"
            return await self.api_client.get("pipelines")

        @self.mcp.tool
        async def list_stages() -> Dict[str, Any]:
            \"\"\"Return a list of pipeline stages.\"\"\"
            return await self.api_client.get("stages")

        @self.mcp.tool
        async def list_milestones() -> Dict[str, Any]:
            \"\"\"Return a list of opportunity milestones.\"\"\"
            return await self.api_client.get("milestones")

        @self.mcp.tool
        async def list_custom_fields() -> Dict[str, Any]:
            \"\"\"Return a list of custom field definitions.\"\"\"
            return await self.api_client.get("fieldDefinitions")

        # Product tools
        @self.mcp.tool
        @paginated_endpoint()
        async def list_products(
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of products.\"\"\"
            params = build_api_params(page=page, per_page=per_page)
            return await self.api_client.get("products", params=params)

        @self.mcp.tool
        @paginated_endpoint()
        async def list_categories(
            page: int = 1,
            per_page: int = 50,
        ) -> Dict[str, Any]:
            \"\"\"Return a paginated list of product categories.\"\"\"
            params = build_api_params(page=page, per_page=per_page)
            return await self.api_client.get("categories", params=params)

        # System tools
        @self.mcp.tool
        async def list_currencies() -> Dict[str, Any]:
            \"\"\"Return a list of supported currencies.\"\"\"
            return await self.api_client.get("currencies")