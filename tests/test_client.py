"""Unit tests for AEM Admin Client."""

import pytest
from unittest.mock import Mock, patch
from aem_admin_client import AEMAdminClient
from aem_admin_client.exceptions import AuthenticationError, ValidationError


class TestAEMAdminClient:
    """Test cases for AEMAdminClient."""

    def test_client_initialization_with_token(self):
        """Test client initialization with auth token."""
        client = AEMAdminClient(auth_token="test-token")
        # Auth token is now stored as a cookie, not header
        assert client._client.session.cookies.get("auth_token") == "test-token"

    def test_client_initialization_with_cookie(self):
        """Test client initialization with auth cookie."""
        client = AEMAdminClient(auth_cookie="test-cookie")
        assert client._client.session.cookies.get("auth_token") == "test-cookie"

    def test_client_initialization_without_auth(self):
        """Test client initialization without authentication raises error."""
        with pytest.raises(ValueError, match="Either auth_token or auth_cookie must be provided"):
            AEMAdminClient()

    def test_client_has_all_operations(self):
        """Test that client has all expected operation modules."""
        client = AEMAdminClient(auth_token="test-token")

        assert hasattr(client, "status")
        assert hasattr(client, "publish")
        assert hasattr(client, "preview")
        assert hasattr(client, "code")
        assert hasattr(client, "cache")
        assert hasattr(client, "index")
        assert hasattr(client, "job")
        assert hasattr(client, "log")
        assert hasattr(client, "snapshot")
        assert hasattr(client, "config")

    def test_context_manager(self):
        """Test client as context manager."""
        with AEMAdminClient(auth_token="test-token") as client:
            assert client is not None
        # Should not raise any exceptions

    @patch('aem_admin_client.base.requests.Session.get')
    def test_status_operation(self, mock_get):
        """Test status operation."""
        # Mock response with proper headers
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {
            "webPath": "/test",
            "resourcePath": "/test.md",
            "live": {"status": 200, "url": "https://example.com/test"}
        }
        mock_response.content = b'{"test": "data"}'
        mock_get.return_value = mock_response

        client = AEMAdminClient(auth_token="test-token")
        status = client.status.get_status("org", "site", "main", "test")

        assert status.web_path == "/test"
        assert status.resource_path == "/test.md"
        assert status.live.status == 200

    @patch('aem_admin_client.base.requests.Session.post')
    def test_publish_operation(self, mock_post):
        """Test publish operation."""
        # Mock response with proper headers
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.reason = "OK"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"status": "published"}
        mock_response.content = b'{"status": "published"}'
        mock_post.return_value = mock_response

        client = AEMAdminClient(auth_token="test-token")
        result = client.publish.publish_resource("org", "site", "main", "test")

        assert result["status"] == "published"

    @patch('aem_admin_client.base.requests.Session.get')
    def test_authentication_error(self, mock_get):
        """Test authentication error handling."""
        # Mock 401 response with proper headers
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.reason = "Unauthorized"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_response.content = b'{"error": "Unauthorized"}'
        mock_get.return_value = mock_response

        client = AEMAdminClient(auth_token="invalid-token")

        with pytest.raises(AuthenticationError):
            client.status.get_status("org", "site", "main", "test")

    @patch('aem_admin_client.base.requests.Session.get')
    def test_validation_error(self, mock_get):
        """Test validation error handling."""
        # Mock 400 response with proper headers
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.reason = "Bad Request"
        mock_response.headers = {"Content-Type": "application/json"}
        mock_response.json.return_value = {"error": "Bad Request"}
        mock_response.content = b'{"error": "Bad Request"}'
        mock_get.return_value = mock_response

        client = AEMAdminClient(auth_token="test-token")

        with pytest.raises(ValidationError):
            client.status.get_status("org", "site", "main", "test")


if __name__ == "__main__":
    pytest.main([__file__])