"""Publish operations for AEM Admin API."""

from typing import Any, Dict, List, Optional

from ..base import BaseClient
from ..models import JobResponse, LiveInfo, PublishRequest


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
            api_path, data=request.dict(by_alias=True, exclude_none=True)
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

        # Convert paths to query parameters instead of request body
        params = {"path": paths} if paths else None
        response_data = self.client.delete(api_path, params=params)
        return JobResponse(**response_data)

    def get_status(self, org: str, site: str) -> Dict[str, Any]:
        """Get publish status.

        Args:
            org: Organization name
            site: Site name

        Returns:
            Publish status response
        """
        path = (
            f"/publish/{self.client._encode_path_param(org)}/"
            f"{self.client._encode_path_param(site)}/status"
        )
        return self.client.get(path)

    def trigger_publish(
        self,
        org: str,
        site: str,
        branch: Optional[str] = None,
        commit: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Trigger publish.

        Args:
            org: Organization name
            site: Site name
            branch: Branch name
            commit: Commit hash

        Returns:
            Publish trigger response
        """
        path = (
            f"/publish/{self.client._encode_path_param(org)}/"
            f"{self.client._encode_path_param(site)}"
        )

        data = {}
        if branch:
            data["branch"] = branch
        if commit:
            data["commit"] = commit

        return self.client.post(path, data=data)

    def cancel_publish(self, org: str, site: str) -> Dict[str, Any]:
        """Cancel publish.

        Args:
            org: Organization name
            site: Site name

        Returns:
            Publish cancel response
        """
        path = (
            f"/publish/{self.client._encode_path_param(org)}/"
            f"{self.client._encode_path_param(site)}"
        )
        return self.client.delete(path)

    def trigger_publish_all(self) -> Dict[str, Any]:
        """Trigger publish for all sites.

        Returns:
            Publish all trigger response
        """
        return self.client.post("/publish")

    def cancel_publish_all(self) -> Dict[str, Any]:
        """Cancel publish for all sites.

        Returns:
            Publish all cancel response
        """
        return self.client.delete("/publish")
