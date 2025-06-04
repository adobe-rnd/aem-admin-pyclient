"""Index operations for AEM Admin API."""

from typing import Any, Dict

from ..base import BaseClient
from ..models import IndexInfo


class IndexOperations:
    """Index operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize index operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_index_status(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> IndexInfo:
        """Get the index status of a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            IndexInfo: Index status information
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/index/{org}/{site}/{ref}/{encoded_path}"

        response_data = self.client.get(api_path)
        return IndexInfo(**response_data)

    def update_index(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Update index for a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Update response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/index/{org}/{site}/{ref}/{encoded_path}"

        return self.client.post(api_path)

    def delete_from_index(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Delete a resource from index.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Delete response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/index/{org}/{site}/{ref}/{encoded_path}"

        return self.client.delete(api_path)
