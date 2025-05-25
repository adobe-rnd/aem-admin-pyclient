# Copyright 2024 AEM Admin Python Client Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Base HTTP client for AEM Admin API."""

import json
import logging
import os
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin, quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .exceptions import (
    AEMAdminError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
    RateLimitError,
    ServerError,
    ValidationError,
)

# Setup logger for this module
logger = logging.getLogger(__name__)


class BaseClient:
    """Base HTTP client for AEM Admin API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None,
        auth_cookie: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3,
        debug: bool = False,
    ):
        """Initialize the base client.

        Args:
            base_url: Base URL for the AEM Admin API (can be overridden by AEM_ADMIN_BASE_URL env var)
            auth_token: Bearer token for authentication (can be overridden by AEM_ADMIN_AUTH_TOKEN env var)
            auth_cookie: Auth cookie for authentication (can be overridden by AEM_ADMIN_AUTH_COOKIE env var)
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            debug: Enable debug logging for HTTP requests/responses
        """
        # Get configuration from environment variables with fallbacks
        self.base_url = (
            os.getenv("AEM_ADMIN_BASE_URL") or
            base_url or
            "https://admin.hlx.page"
        ).rstrip("/")

        auth_token = os.getenv("AEM_ADMIN_AUTH_TOKEN") or auth_token
        auth_cookie = os.getenv("AEM_ADMIN_AUTH_COOKIE") or auth_cookie

        self.timeout = timeout
        self.debug = debug

        # Setup session with retry strategy
        self.session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        # Setup authentication
        if auth_token:
            self.session.cookies.set("auth_token", auth_token)
        elif auth_cookie:
            self.session.cookies.set("auth_token", auth_cookie)

        # Default headers
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "aem-admin-python-client/1.0.0",
        })

        # Configure logging based on environment variables and debug flag
        self._configure_logging()

    def _get_log_level_from_env(self) -> int:
        """Get log level from environment variables.

        Checks the following environment variables in order:
        1. AEM_ADMIN_LOG_LEVEL - specific to this client
        2. LOG_LEVEL - general log level
        3. PYTHON_LOG_LEVEL - Python-specific log level

        Returns:
            Log level as integer (defaults to INFO if debug=False, DEBUG if debug=True)
        """
        # Environment variable names to check in order of priority
        env_vars = ["AEM_ADMIN_LOG_LEVEL", "LOG_LEVEL", "PYTHON_LOG_LEVEL"]

        for env_var in env_vars:
            log_level_str = os.getenv(env_var)
            if log_level_str:
                # Convert string to log level
                log_level_str = log_level_str.upper()
                if hasattr(logging, log_level_str):
                    return getattr(logging, log_level_str)
                else:
                    # Try to parse as integer
                    try:
                        return int(log_level_str)
                    except ValueError:
                        logger.warning(f"Invalid log level '{log_level_str}' in {env_var}, ignoring")

        # Default based on debug flag
        return logging.DEBUG if self.debug else logging.INFO

    def _configure_logging(self) -> None:
        """Configure logging based on environment variables and debug settings."""
        log_level = self._get_log_level_from_env()

        # Configure root logger if not already configured
        root_logger = logging.getLogger()
        if not root_logger.handlers:
            logging.basicConfig(
                level=log_level,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

        # Set level for this module's logger
        logger.setLevel(log_level)

        # Configure urllib3 logging for detailed HTTP logs if debug level
        if log_level <= logging.DEBUG:
            logging.getLogger("urllib3.connectionpool").setLevel(logging.DEBUG)
            # Also enable requests debugging
            logging.getLogger("requests.packages.urllib3").setLevel(logging.DEBUG)

        # Log the current configuration
        logger.info(f"AEM Admin Client logging configured at level: {logging.getLevelName(log_level)}")

    def _build_url(self, path: str) -> str:
        """Build full URL from path."""
        return urljoin(self.base_url, path.lstrip("/"))

    def _encode_path_param(self, param: str) -> str:
        """URL encode path parameter."""
        return quote(param, safe="")

    def _log_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        data: Any = None,
    ) -> None:
        """Log HTTP request details."""
        if not logger.isEnabledFor(logging.DEBUG):
            return

        logger.debug(f"HTTP Request: {method} {url}")

        if params:
            logger.debug(f"Request params: {params}")

        if headers:
            # Mask sensitive headers
            safe_headers = {}
            for key, value in headers.items():
                if key.lower() in ['authorization', 'cookie']:
                    safe_headers[key] = "***MASKED***"
                else:
                    safe_headers[key] = value
            logger.debug(f"Request headers: {safe_headers}")

        if data:
            if isinstance(data, (dict, list)):
                logger.debug(f"Request body: {json.dumps(data, indent=2)}")
            else:
                logger.debug(f"Request body: {data}")

    def _log_response(self, response: requests.Response) -> None:
        """Log HTTP response details."""
        if not logger.isEnabledFor(logging.DEBUG):
            return

        logger.debug(f"HTTP Response: {response.status_code} {response.reason}")
        logger.debug(f"Response headers: {dict(response.headers)}")

        if response.content:
            try:
                response_json = response.json()
                logger.debug(f"Response body: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                # Log first 1000 characters of text response
                content = response.text[:1000]
                if len(response.text) > 1000:
                    content += "... (truncated)"
                logger.debug(f"Response body (text): {content}")
        else:
            logger.debug("Response body: (empty)")

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        self._log_response(response)

        try:
            response_data = response.json() if response.content else {}
        except json.JSONDecodeError:
            response_data = {"text": response.text}

        if response.status_code == 200:
            return response_data
        elif response.status_code == 201:
            return response_data
        elif response.status_code == 202:
            return response_data
        elif response.status_code == 204:
            return {}
        elif response.status_code == 400:
            raise ValidationError(
                "Invalid request",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 401:
            raise AuthenticationError(
                "Authentication failed",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 403:
            raise AuthorizationError(
                "Access forbidden",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 404:
            raise NotFoundError(
                "Resource not found",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 409:
            raise ConflictError(
                "Conflict",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code == 429:
            raise RateLimitError(
                "Rate limit exceeded",
                status_code=response.status_code,
                response_data=response_data,
            )
        elif response.status_code >= 500:
            raise ServerError(
                "Server error",
                status_code=response.status_code,
                response_data=response_data,
            )
        else:
            raise AEMAdminError(
                f"Unexpected status code: {response.status_code}",
                status_code=response.status_code,
                response_data=response_data,
            )

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make GET request."""
        url = self._build_url(path)

        # Merge headers with session headers for logging
        request_headers = {**self.session.headers}
        if headers:
            request_headers.update(headers)

        self._log_request("GET", url, request_headers, params)

        response = self.session.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    def post(
        self,
        path: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make POST request."""
        url = self._build_url(path)

        # Handle data and headers appropriately
        if data is None:
            # No data provided - send empty JSON object and ensure proper content type
            json_data = {}
            data_to_send = None
            # Don't override content-type if explicitly provided in headers
            if not headers or "Content-Type" not in headers:
                headers = headers or {}
                headers["Content-Type"] = "application/json"
        elif isinstance(data, dict):
            json_data = data
            data_to_send = None
        else:
            json_data = None
            data_to_send = data

        # Merge headers with session headers for logging
        request_headers = {**self.session.headers}
        if headers:
            request_headers.update(headers)

        self._log_request("POST", url, request_headers, params, json_data or data_to_send)

        response = self.session.post(
            url,
            json=json_data,
            data=data_to_send,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    def put(
        self,
        path: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request."""
        url = self._build_url(path)

        # Handle data and headers appropriately
        if data is None:
            # No data provided - send empty JSON object and ensure proper content type
            json_data = {}
            data_to_send = None
            # Don't override content-type if explicitly provided in headers
            if not headers or "Content-Type" not in headers:
                headers = headers or {}
                headers["Content-Type"] = "application/json"
        elif isinstance(data, dict):
            json_data = data
            data_to_send = None
        else:
            json_data = None
            data_to_send = data

        # Merge headers with session headers for logging
        request_headers = {**self.session.headers}
        if headers:
            request_headers.update(headers)

        self._log_request("PUT", url, request_headers, params, json_data or data_to_send)

        response = self.session.put(
            url,
            json=json_data,
            data=data_to_send,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)

    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make DELETE request."""
        url = self._build_url(path)

        # Merge headers with session headers for logging
        request_headers = {**self.session.headers}
        if headers:
            request_headers.update(headers)

        self._log_request("DELETE", url, request_headers, params)

        response = self.session.delete(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )
        return self._handle_response(response)