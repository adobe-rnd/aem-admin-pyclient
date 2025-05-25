"""Snapshot operations for AEM Admin API."""

from typing import Optional, List, Dict, Any
from ..base import BaseClient
from ..models import SnapshotInfo, SnapshotRequest


class SnapshotOperations:
    """Snapshot operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize snapshot operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def list_snapshots(
        self,
        org: str,
        site: str,
        ref: str,
    ) -> List[SnapshotInfo]:
        """List all snapshots for a site.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)

        Returns:
            List[SnapshotInfo]: List of snapshots
        """
        api_path = f"/snapshot/{org}/{site}/{ref}"

        response_data = self.client.get(api_path)
        return [SnapshotInfo(**snapshot) for snapshot in response_data.get("snapshots", [])]

    def create_snapshot(
        self,
        org: str,
        site: str,
        ref: str,
        request: SnapshotRequest,
        filter_type: Optional[str] = None,
        publish: Optional[bool] = None,
    ) -> SnapshotInfo:
        """Create a new snapshot.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            request: Snapshot creation request
            filter_type: Filter type ('all' or 'modified')
            publish: Whether to publish the snapshot

        Returns:
            SnapshotInfo: Created snapshot information
        """
        api_path = f"/snapshot/{org}/{site}/{ref}"

        params = {}
        if filter_type:
            params["filter"] = filter_type
        if publish:
            params["publish"] = "true"

        response_data = self.client.post(
            api_path,
            data=request.dict(by_alias=True, exclude_none=True),
            params=params
        )
        return SnapshotInfo(**response_data)

    def get_snapshot(
        self,
        org: str,
        site: str,
        ref: str,
        snapshot_id: str,
    ) -> SnapshotInfo:
        """Get information about a specific snapshot.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            snapshot_id: Snapshot ID

        Returns:
            SnapshotInfo: Snapshot information
        """
        api_path = f"/snapshot/{org}/{site}/{ref}/{snapshot_id}"

        response_data = self.client.get(api_path)
        return SnapshotInfo(**response_data)

    def delete_snapshot(
        self,
        org: str,
        site: str,
        ref: str,
        snapshot_id: str,
    ) -> Dict[str, Any]:
        """Delete a snapshot.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            snapshot_id: Snapshot ID

        Returns:
            Dict: Delete response
        """
        api_path = f"/snapshot/{org}/{site}/{ref}/{snapshot_id}"

        return self.client.delete(api_path)

    def review_snapshot(
        self,
        org: str,
        site: str,
        ref: str,
        snapshot_id: str,
        review_action: str,
        message: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Review a snapshot (request, approve, or reject).

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            snapshot_id: Snapshot ID
            review_action: Review action ('request', 'approve', 'reject')
            message: Optional review message

        Returns:
            Dict: Review response
        """
        api_path = f"/snapshot/{org}/{site}/{ref}/{snapshot_id}"

        params = {"review": review_action}
        if message:
            params["message"] = message

        return self.client.post(api_path, params=params)