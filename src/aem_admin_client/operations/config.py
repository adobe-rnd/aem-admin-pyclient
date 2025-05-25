"""Configuration operations for AEM Admin API."""

from typing import Optional, List, Dict, Any
from ..base import BaseClient
from ..models import ConfigResponse, SiteConfig, OrgConfig, ProfileConfig


class ConfigOperations:
    """Configuration operations for AEM Admin API."""

    def __init__(self, client: BaseClient):
        """Initialize config operations.

        Args:
            client: Base HTTP client instance
        """
        self.client = client

    # Organization Configuration
    def get_org_config(self, org: str) -> OrgConfig:
        """Get organization configuration.

        Args:
            org: Organization name

        Returns:
            OrgConfig: Organization configuration
        """
        api_path = f"/config/{org}.json"

        response_data = self.client.get(api_path)
        return OrgConfig(**response_data)

    def update_org_config(self, org: str, config: OrgConfig) -> OrgConfig:
        """Update organization configuration.

        Args:
            org: Organization name
            config: Organization configuration

        Returns:
            OrgConfig: Updated organization configuration
        """
        api_path = f"/config/{org}.json"

        response_data = self.client.put(
            api_path,
            data=config.dict(by_alias=True, exclude_none=True)
        )
        return OrgConfig(**response_data)

    # Site Configuration
    def get_site_config(self, org: str, site: str) -> SiteConfig:
        """Get site configuration.

        Args:
            org: Organization name
            site: Site ID

        Returns:
            SiteConfig: Site configuration
        """
        api_path = f"/config/{org}/sites/{site}.json"

        response_data = self.client.get(api_path)
        return SiteConfig(**response_data)

    def update_site_config(self, org: str, site: str, config: SiteConfig) -> SiteConfig:
        """Update site configuration.

        Args:
            org: Organization name
            site: Site ID
            config: Site configuration

        Returns:
            SiteConfig: Updated site configuration
        """
        api_path = f"/config/{org}/sites/{site}.json"

        response_data = self.client.put(
            api_path,
            data=config.dict(by_alias=True, exclude_none=True)
        )
        return SiteConfig(**response_data)

    def delete_site_config(self, org: str, site: str) -> Dict[str, Any]:
        """Delete site configuration.

        Args:
            org: Organization name
            site: Site ID

        Returns:
            Dict: Delete response
        """
        api_path = f"/config/{org}/sites/{site}.json"

        return self.client.delete(api_path)

    # Profile Configuration
    def get_profile_config(self, org: str, profile: str) -> ProfileConfig:
        """Get profile configuration.

        Args:
            org: Organization name
            profile: Profile name

        Returns:
            ProfileConfig: Profile configuration
        """
        api_path = f"/config/{org}/profiles/{profile}.json"

        response_data = self.client.get(api_path)
        return ProfileConfig(**response_data)

    def update_profile_config(
        self,
        org: str,
        profile: str,
        config: ProfileConfig
    ) -> ProfileConfig:
        """Update profile configuration.

        Args:
            org: Organization name
            profile: Profile name
            config: Profile configuration

        Returns:
            ProfileConfig: Updated profile configuration
        """
        api_path = f"/config/{org}/profiles/{profile}.json"

        response_data = self.client.put(
            api_path,
            data=config.dict(by_alias=True, exclude_none=True)
        )
        return ProfileConfig(**response_data)

    def delete_profile_config(self, org: str, profile: str) -> Dict[str, Any]:
        """Delete profile configuration.

        Args:
            org: Organization name
            profile: Profile name

        Returns:
            Dict: Delete response
        """
        api_path = f"/config/{org}/profiles/{profile}.json"

        return self.client.delete(api_path)

    # Generic Configuration Methods
    def get_config(self, path: str) -> ConfigResponse:
        """Get configuration at a specific path.

        Args:
            path: Configuration path (e.g., 'org/sites/site/cdn/prod.json')

        Returns:
            ConfigResponse: Configuration data
        """
        api_path = f"/config/{path}"

        response_data = self.client.get(api_path)
        return ConfigResponse(**response_data)

    def update_config(self, path: str, data: Dict[str, Any]) -> ConfigResponse:
        """Update configuration at a specific path.

        Args:
            path: Configuration path
            data: Configuration data

        Returns:
            ConfigResponse: Updated configuration data
        """
        api_path = f"/config/{path}"

        response_data = self.client.put(api_path, data=data)
        return ConfigResponse(**response_data)

    def delete_config(self, path: str) -> Dict[str, Any]:
        """Delete configuration at a specific path.

        Args:
            path: Configuration path

        Returns:
            Dict: Delete response
        """
        api_path = f"/config/{path}"

        return self.client.delete(api_path)