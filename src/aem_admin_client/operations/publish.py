"""Publish operations for AEM Admin API."""

from typing import Optional, List, Dict, Any
from ..base import BaseClient
from ..models import LiveInfo, PublishRequest, JobResponse


class PublishOperations:
    """Publish operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize publish operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_publish_status(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> LiveInfo:
        """Get the publish status of a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            LiveInfo: Publish status information
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/live/{org}/{site}/{ref}/{encoded_path}"

        response_data = self.client.get(api_path)
        return LiveInfo(**response_data)

    def publish_resource(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
        force_update_redirects: Optional[bool] = None,
        disable_notifications: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """Publish a single resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource
            force_update_redirects: Force update of redirects
            disable_notifications: Disable notifications

        Returns:
            Dict: Publish response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/live/{org}/{site}/{ref}/{encoded_path}"

        params = {}
        if force_update_redirects is not None:
            params["forceUpdateRedirects"] = force_update_redirects
        if disable_notifications is not None:
            params["disableNotifications"] = disable_notifications

        return self.client.post(api_path, params=params)

    def unpublish_resource(
        self,
        org: str,
        site: str,
        ref: str,
        path: str,
    ) -> Dict[str, Any]:
        """Unpublish a resource.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            path: Relative path of the resource

        Returns:
            Dict: Unpublish response
        """
        encoded_path = self.client._encode_path_param(path)
        api_path = f"/live/{org}/{site}/{ref}/{encoded_path}"

        return self.client.delete(api_path)

    def bulk_publish(
        self,
        org: str,
        site: str,
        ref: str,
        request: PublishRequest,
    ) -> JobResponse:
        """Start a bulk publish job.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            request: Bulk publish request

        Returns:
            JobResponse: Information about the created job
        """
        api_path = f"/live/{org}/{site}/{ref}/*"

        response_data = self.client.post(
            api_path,
            data=request.dict(by_alias=True, exclude_none=True)
        )
        return JobResponse(**response_data)

    def bulk_unpublish(
        self,
        org: str,
        site: str,
        ref: str,
        paths: List[str],
    ) -> JobResponse:
        """Start a bulk unpublish job.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            paths: List of paths to unpublish

        Returns:
            JobResponse: Information about the created job
        """
        api_path = f"/live/{org}/{site}/{ref}/*"

        request_data = {"paths": paths}
        response_data = self.client.delete(api_path, data=request_data)
        return JobResponse(**response_data)