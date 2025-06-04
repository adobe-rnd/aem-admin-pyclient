"""Custom exceptions for AEM Admin Client."""

from typing import Any, Dict, Optional


class AEMAdminError(Exception):
    """Base exception for AEM Admin API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(AEMAdminError):
    """Raised when authentication fails (401)."""

    pass


class AuthorizationError(AEMAdminError):
    """Raised when authorization fails (403)."""

    pass


class NotFoundError(AEMAdminError):
    """Raised when a resource is not found (404)."""

    pass


class ConflictError(AEMAdminError):
    """Raised when there's a conflict (409)."""

    pass


class RateLimitError(AEMAdminError):
    """Raised when rate limit is exceeded (429)."""

    pass


class ServerError(AEMAdminError):
    """Raised when server error occurs (5xx)."""

    pass


class ValidationError(AEMAdminError):
    """Raised when request validation fails."""

    pass
