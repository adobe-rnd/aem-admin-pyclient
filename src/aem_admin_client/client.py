# Copyright 2024 AEM Admin Python Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Main AEM Admin Client."""

from typing import Any, Dict, Optional

from .base import BaseClient
from .operations import (
    CacheOperations,
    CodeOperations,
    ConfigOperations,
    IndexOperations,
    JobOperations,
    LogOperations,
    PreviewOperations,
    PublishOperations,
    SnapshotOperations,
    StatusOperations,
)


class AEMAdminClient:
    """Main client for AEM Admin API.

    This client provides access to all AEM Admin API operations through
    organized operation modules.

    Example:
        >>> client = AEMAdminClient(auth_token="your-token")
        >>> status = client.status.get_status("org", "site", "main", "index")
        >>> client.publish.publish_resource("org", "site", "main", "index")
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None,
        auth_cookie: Optional[str] = None,
        debug: bool = False,
    ) -> None:
        """Initialize the AEM Admin client.

        Args:
            base_url: Base URL for the AEM Admin API
            auth_token: Bearer token for authentication
            auth_cookie: Auth cookie for authentication
            debug: Enable debug logging

        Raises:
            ValueError: If neither auth_token nor auth_cookie is provided
        """
        if not auth_token and not auth_cookie:
            raise ValueError("Either auth_token or auth_cookie must be provided")

        # Initialize base HTTP client
        self.client = BaseClient(
            base_url=base_url,
            auth_token=auth_token,
            auth_cookie=auth_cookie,
            debug=debug,
        )

        # Initialize operation modules
        self.status = StatusOperations(self.client)
        self.publish = PublishOperations(self.client)
        self.preview = PreviewOperations(self.client)
        self.code = CodeOperations(self.client)
        self.cache = CacheOperations(self.client)
        self.index = IndexOperations(self.client)
        self.job = JobOperations(self.client)
        self.log = LogOperations(self.client)
        self.snapshot = SnapshotOperations(self.client)
        self.config = ConfigOperations(self.client)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make a direct request to the API.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            headers: Request headers

        Returns:
            API response data
        """
        return self.client.request(
            method=method,
            endpoint=endpoint,
            params=params,
            data=data,
            headers=headers,
        )

    def close(self) -> None:
        """Close the HTTP session."""
        if hasattr(self.client, "session"):
            self.client.session.close()

    def __enter__(self) -> "AEMAdminClient":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
