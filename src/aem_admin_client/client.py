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

from typing import Optional

from .base import BaseClient
from .operations import (
    StatusOperations,
    PublishOperations,
    PreviewOperations,
    CodeOperations,
    CacheOperations,
    IndexOperations,
    JobOperations,
    LogOperations,
    SnapshotOperations,
    ConfigOperations,
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
        base_url: str = "https://admin.hlx.page",
        auth_token: Optional[str] = None,
        auth_cookie: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
    ):
        """Initialize the AEM Admin client.

        Args:
            base_url: Base URL for the AEM Admin API
            auth_token: Bearer token for authentication
            auth_cookie: Auth cookie for authentication
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests

        Raises:
            ValueError: If neither auth_token nor auth_cookie is provided
        """
        if not auth_token and not auth_cookie:
            raise ValueError("Either auth_token or auth_cookie must be provided")

        # Initialize base HTTP client
        self._client = BaseClient(
            base_url=base_url,
            auth_token=auth_token,
            auth_cookie=auth_cookie,
            timeout=timeout,
            max_retries=max_retries,
        )

        # Initialize operation modules
        self.status = StatusOperations(self._client)
        self.publish = PublishOperations(self._client)
        self.preview = PreviewOperations(self._client)
        self.code = CodeOperations(self._client)
        self.cache = CacheOperations(self._client)
        self.index = IndexOperations(self._client)
        self.job = JobOperations(self._client)
        self.log = LogOperations(self._client)
        self.snapshot = SnapshotOperations(self._client)
        self.config = ConfigOperations(self._client)

    def close(self):
        """Close the HTTP session."""
        if hasattr(self._client, 'session'):
            self._client.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()