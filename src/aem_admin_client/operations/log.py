"""Log operations for AEM Admin API."""

from typing import Optional

from ..base import BaseClient
from ..models import LogResponse


class LogOperations:
    """Log operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize log operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_logs(
        self,
        org: str,
        site: str,
        ref: str,
        from_time: Optional[str] = None,
        to_time: Optional[str] = None,
        since: Optional[str] = None,
        next_token: Optional[str] = None,
    ) -> LogResponse:
        """Get logs for a site.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            from_time: Starting date to get logs from
            to_time: Ending date to get logs from
            since: Time span to retrieve logs for (e.g., '5m', '1h', '1d')
            next_token: Token from previous call to continue

        Returns:
            LogResponse: Log entries and pagination info
        """
        api_path = f"/log/{org}/{site}/{ref}"

        params = {}
        if from_time:
            params["from"] = from_time
        if to_time:
            params["to"] = to_time
        if since:
            params["since"] = since
        if next_token:
            params["nextToken"] = next_token

        response_data = self.client.get(api_path, params=params)
        return LogResponse(**response_data)
