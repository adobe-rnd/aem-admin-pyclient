"""Job operations for AEM Admin API."""

from typing import Any, Dict, List

from ..base import BaseClient
from ..models import JobInfo


class JobOperations:
    """Job operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize job operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    def get_job(
        self,
        org: str,
        site: str,
        ref: str,
        topic: str,
        job_name: str,
    ) -> JobInfo:
        """Get information about a specific job.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            topic: Job topic
            job_name: Job name

        Returns:
            JobInfo: Job information
        """
        api_path = f"/job/{org}/{site}/{ref}/{topic}/{job_name}"

        response_data = self.client.get(api_path)
        return JobInfo(**response_data)

    def list_jobs(
        self,
        org: str,
        site: str,
        ref: str,
        topic: str,
    ) -> List[JobInfo]:
        """List jobs for a specific topic.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            topic: Job topic

        Returns:
            List[JobInfo]: List of jobs
        """
        api_path = f"/job/{org}/{site}/{ref}/{topic}"

        response_data = self.client.get(api_path)
        return [JobInfo(**job) for job in response_data.get("jobs", [])]

    def delete_job(
        self,
        org: str,
        site: str,
        ref: str,
        topic: str,
        job_name: str,
    ) -> Dict[str, Any]:
        """Delete a specific job.

        Args:
            org: Organization name
            site: Site ID
            ref: Repository reference (branch)
            topic: Job topic
            job_name: Job name

        Returns:
            Dict: Delete response
        """
        api_path = f"/job/{org}/{site}/{ref}/{topic}/{job_name}"

        return self.client.delete(api_path)
