"""Configuration management for AEM Admin Client."""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for AEM Admin Client."""

    @staticmethod
    def get_auth_token() -> Optional[str]:
        """Get authentication token from environment."""
        return os.getenv("AEM_AUTH_TOKEN")

    @staticmethod
    def get_auth_cookie() -> Optional[str]:
        """Get authentication cookie from environment."""
        return os.getenv("AEM_AUTH_COOKIE")

    @staticmethod
    def get_base_url() -> str:
        """Get base URL from environment."""
        return os.getenv("AEM_BASE_URL", "https://admin.hlx.page")

    @staticmethod
    def get_timeout() -> int:
        """Get timeout from environment."""
        return int(os.getenv("AEM_TIMEOUT", "30"))

    @staticmethod
    def get_default_org() -> Optional[str]:
        """Get default organization from environment."""
        return os.getenv("AEM_DEFAULT_ORG")

    @staticmethod
    def get_default_site() -> Optional[str]:
        """Get default site from environment."""
        return os.getenv("AEM_DEFAULT_SITE")

    @staticmethod
    def get_log_level() -> str:
        """Get log level from environment."""
        return os.getenv("LOG_LEVEL", "INFO").upper()


def get_client_from_env(**kwargs):
    """
    Create an AEMAdminClient instance using environment variables.

    Args:
        **kwargs: Additional arguments to override environment settings

    Returns:
        AEMAdminClient: Configured client instance

    Raises:
        ValueError: If no authentication method is provided
    """
    from .client import AEMAdminClient

    # Get values from environment, allow kwargs to override
    auth_token = kwargs.get("auth_token") or Config.get_auth_token()
    auth_cookie = kwargs.get("auth_cookie") or Config.get_auth_cookie()
    base_url = kwargs.get("base_url") or Config.get_base_url()
    timeout = kwargs.get("timeout") or Config.get_timeout()

    if not auth_token and not auth_cookie:
        raise ValueError(
            "No authentication method provided. Set AEM_AUTH_TOKEN or AEM_AUTH_COOKIE "
            "environment variable, or pass auth_token/auth_cookie as arguments."
        )

    return AEMAdminClient(
        base_url=base_url,
        auth_token=auth_token,
        auth_cookie=auth_cookie,
        timeout=timeout,
        **{k: v for k, v in kwargs.items()
           if k not in ["auth_token", "auth_cookie", "base_url", "timeout"]}
    )
