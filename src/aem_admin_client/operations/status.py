"""Status operations for AEM Admin API."""

from typing import Optional, List
from ..base import BaseClient
from ..models import StatusResponse, BulkStatusRequest, JobResponse


class StatusOperations:
    """Status operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize status operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_status(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
        edit_url: Optional[str] = None,
    ) -> StatusResponse:
        """Get the overall status of a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource
            edit_url: Optional URL of the edit document or 'auto'

        Returns:
            StatusResponse: Complete status information
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/status/{org}/{site}/{ref}/{encoded_path}"

        params = {}
        if edit_url:
            params["editUrl"] = edit_url

        response_data = self.client.get(api_path, params=params)
        return StatusResponse(**response_data)

    def bulk_status(
        self,
        org: str,
        site: str,
        ref: str,
        request: BulkStatusRequest,
    ) -> JobResponse:
        """Start a bulk status job for multiple resources.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            request: Bulk status request with paths and options

        Returns:
            JobResponse: Information about the created job
        """
        api_path = f"/status/{org}/{site}/{ref}/*"

        response_data = self.client.post(
            api_path,
            data=request.dict(by_alias=True, exclude_none=True)
        )
        return JobResponse(**response_data)