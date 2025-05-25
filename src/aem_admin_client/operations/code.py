"""Code operations for AEM Admin API."""

from typing import Optional, Dict, Any
from ..base import BaseClient
from ..models import CodeInfo


class CodeOperations:
    """Code operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize code operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_code_status(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> CodeInfo:
        """Get the code status of a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            CodeInfo: Code status information
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/code/{org}/{site}/{ref}/{encoded_path}"

        response_data = self.client.get(api_path)
        return CodeInfo(**response_data)

    def update_code(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Update code for a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Update response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/code/{org}/{site}/{ref}/{encoded_path}"

        return self.client.post(api_path)

    def delete_code(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Delete code for a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Delete response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/code/{org}/{site}/{ref}/{encoded_path}"

        return self.client.delete(api_path)
