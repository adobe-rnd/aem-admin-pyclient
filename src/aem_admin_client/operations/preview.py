"""Preview operations for AEM Admin API."""

from typing import Optional, List, Dict, Any
from ..base import BaseClient
from ..models import PreviewInfo, PreviewRequest, JobResponse


class PreviewOperations:
    """Preview operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize preview operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_preview_status(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> PreviewInfo:
        """Get the preview status of a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            PreviewInfo: Preview status information
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/preview/{org}/{site}/{ref}/{encoded_path}"

        response_data = self.client.get(api_path)
        return PreviewInfo(**response_data)

    def preview_resource(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
        word2md_version: Optional[str] = None,
        gdocs2md_version: Optional[str] = None,
        html2md_version: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Preview a single resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource
            word2md_version: Version for word2md service
            gdocs2md_version: Version for gdocs2md service
            html2md_version: Version for html2md service

        Returns:
            Dict: Preview response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/preview/{org}/{site}/{ref}/{encoded_path}"

        params = {}
        if word2md_version:
            params["hlx-word2md-version"] = word2md_version
        if gdocs2md_version:
            params["hlx-gdocs2md-version"] = gdocs2md_version
        if html2md_version:
            params["hlx-html2md-version"] = html2md_version

        return self.client.post(api_path, params=params)

    def delete_preview(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Delete a preview resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Delete response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/preview/{org}/{site}/{ref}/{encoded_path}"

        return self.client.delete(api_path)

    def bulk_preview(
        self,
        org: str,
        site: str,
        ref: str,
        request: PreviewRequest,
    ) -> JobResponse:
        """Start a bulk preview job.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            request: Bulk preview request

        Returns:
            JobResponse: Information about the created job
        """
        api_path = f"/preview/{org}/{site}/{ref}/*"

        response_data = self.client.post(
            api_path,
            data=request.dict(by_alias=True, exclude_none=True)
        )
        return JobResponse(**response_data)

    def bulk_delete_preview(
        self,
        org: str,
        site: str,
        ref: str,
        paths: List[str],
    ) -> JobResponse:
        """Start a bulk preview deletion job.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            paths: List of paths to delete from preview

        Returns:
            JobResponse: Information about the created job
        """
        api_path = f"/preview/{org}/{site}/{ref}/*"

        request_data = {"paths": paths}
        response_data = self.client.delete(api_path, data=request_data)
        return JobResponse(**response_data)