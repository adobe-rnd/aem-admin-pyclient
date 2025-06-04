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

"""Base HTTP client with debug logging."""

import json
import logging
import os
from typing import Any, Dict, Optional, Union
from urllib.parse import quote, urljoin

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import Config
from .exceptions import (
    AEMAdminError,
    AuthenticationError,
    AuthorizationError,
    ConflictError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class BaseClient:
    """Base client with common HTTP functionality."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        auth_token: Optional[str] = None,
        auth_cookie: Optional[str] = None,
        debug: bool = False,
    ) -> None:
        """Initialize the base client."""
        self.base_url = base_url or Config.get_base_url()
        self.session = self._create_session()
        self._setup_auth(auth_token, auth_cookie)
        self._setup_logging(debug)

    def _create_session(self) -> requests.Session:
        """Create and configure requests session with retries."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def _setup_auth(
        self,
        auth_token: Optional[str],
        auth_cookie: Optional[str]
    ) -> None:
        """Set up authentication using either token or cookie."""
        if auth_token:
            self.session.cookies.set("auth_token", str(auth_token))
        elif auth_cookie:
            self.session.cookies.set("auth_token", str(auth_cookie))
        elif os.getenv("AEM_ADMIN_AUTH_TOKEN"):
            self.session.cookies.set(
                "auth_token",
                str(os.getenv("AEM_ADMIN_AUTH_TOKEN"))
            )
        elif os.getenv("AEM_ADMIN_AUTH_COOKIE"):
            self.session.cookies.set(
                "auth_token",
                str(os.getenv("AEM_ADMIN_AUTH_COOKIE"))
            )

    def _setup_logging(self, debug: bool) -> None:
        """Set up logging configuration."""
        self.logger = logging.getLogger(__name__)
        log_level = Config.get_log_level() if debug else logging.WARNING
        self.logger.setLevel(log_level)

    def _get_url(self, endpoint: str) -> str:
        """Build full URL for the endpoint."""
        return urljoin(self.base_url, endpoint)

    def _encode_path_param(self, param: str) -> str:
        """URL encode path parameter."""
        return quote(param, safe="")

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make GET request."""
        return self.request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make POST request."""
        return self.request("POST", path, data=data, params=params, headers=headers)

    def put(
        self,
        path: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make PUT request."""
        return self.request("PUT", path, data=data, params=params, headers=headers)

    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make DELETE request."""
        return self.request("DELETE", path, params=params, headers=headers)

    def _log_request(self, method: str, url: str, **kwargs: Any) -> None:
        """Log request details at debug level."""
        if not self.logger.isEnabledFor(logging.DEBUG):
            return

        headers = kwargs.get("headers", {}).copy()
        if "Cookie" in headers:
            headers["Cookie"] = "***"
        if "Authorization" in headers:
            headers["Authorization"] = "***"

        msg = [
            f"Request: {method} {url}",
            f"Headers: {headers}",
            f"Params: {kwargs.get('params')}",
            f"Data: {kwargs.get('data')}",
        ]
        self.logger.debug("\n".join(msg))

    def _log_response(self, response: requests.Response) -> None:
        """Log response details at debug level."""
        if not self.logger.isEnabledFor(logging.DEBUG):
            return

        content = response.text[:1000]
        if len(response.text) > 1000:
            content += "..."

        self.logger.debug(
            "Response: %s\nHeaders: %s\nContent: %s",
            response.status_code,
            response.headers,
            content,
        )

    def _handle_error_response(
        self,
        status_code: int,
        data: Dict[str, Any]
    ) -> None:
        """Handle error responses and raise appropriate exceptions."""
        error_mapping = {
            400: (ValidationError, "Invalid request parameters"),
            401: (AuthenticationError, "Authentication failed"),
            403: (AuthorizationError, "Authorization failed"),
            404: (NotFoundError, "Resource not found"),
            409: (ConflictError, "Resource conflict"),
            429: (RateLimitError, "Rate limit exceeded"),
        }

        if status_code in error_mapping:
            exc_class, message = error_mapping[status_code]
            raise exc_class(message, response_data=data, status_code=status_code)
        elif status_code >= 500:
            raise ServerError(
                "Server error",
                response_data=data,
                status_code=status_code
            )
        else:
            raise AEMAdminError(
                f"Unexpected status code: {status_code}",
                response_data=data,
                status_code=status_code,
            )

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        self._log_response(response)

        try:
            data = response.json() if response.content else {}
        except json.JSONDecodeError:
            data = {"error": "Invalid JSON response", "detail": response.text}

        if response.status_code in (200, 201, 202, 204):
            return data if data else {}

        self._handle_error_response(response.status_code, data)
        return {}  # This line is never reached but satisfies mypy

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], str]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Make HTTP request to the API."""
        url = self._get_url(endpoint)
        request_headers = {"Accept": "application/json"}
        if headers:
            request_headers.update(headers)

        if isinstance(data, dict):
            request_headers["Content-Type"] = "application/json"
            data = json.dumps(data)

        kwargs = {
            "headers": request_headers,
            "params": params,
            "data": data,
        }
        self._log_request(method, url, **kwargs)

        response = self.session.request(
            method,
            url,
            params=params,
            data=data,
            headers=request_headers,
        )

        return self._handle_response(response)
