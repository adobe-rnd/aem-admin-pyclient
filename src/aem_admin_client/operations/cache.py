"""Cache operations for AEM Admin API."""

from typing import Optional, Dict, Any
from ..base import BaseClient
from ..models import CacheInfo


class CacheOperations:
    """Cache operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize cache operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_cache_status(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> CacheInfo:
        """Get the cache status of a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            CacheInfo: Cache status information
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/cache/{org}/{site}/{ref}/{encoded_path}"

        response_data = self.client.get(api_path)
        return CacheInfo(**response_data)

    def purge_cache(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Purge cache for a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Purge response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/cache/{org}/{site}/{ref}/{encoded_path}"

        return self.client.post(api_path)