"""
Tests for Google Workspace service module.
"""

from unittest.mock import MagicMock, patch

from gmail_mcp_server.services.google_workspace_service import (
    get_gmail_api_service,
    get_google_drive_api_service,
)


class TestGetGmailApiService:
    """Tests for get_gmail_api_service function."""

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_builds_gmail_service(self, mock_get_creds, mock_build):
        """Test building Gmail API service."""
        mock_credentials = MagicMock()
        mock_get_creds.return_value = mock_credentials
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        result = get_gmail_api_service()

        mock_get_creds.assert_called_once()
        mock_build.assert_called_once_with("gmail", "v1", credentials=mock_credentials)
        assert result == mock_service

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_uses_correct_api_version(self, mock_get_creds, mock_build):
        """Test that correct API version is used."""
        mock_credentials = MagicMock()
        mock_get_creds.return_value = mock_credentials

        get_gmail_api_service()

        args, kwargs = mock_build.call_args
        assert args[0] == "gmail"
        assert args[1] == "v1"

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_passes_credentials_to_build(self, mock_get_creds, mock_build):
        """Test that credentials are passed to build function."""
        mock_credentials = MagicMock()
        mock_get_creds.return_value = mock_credentials

        get_gmail_api_service()

        args, kwargs = mock_build.call_args
        assert kwargs["credentials"] == mock_credentials


class TestGetGoogleDriveApiService:
    """Tests for get_google_drive_api_service function."""

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_builds_drive_service(self, mock_get_creds, mock_build):
        """Test building Google Drive API service."""
        mock_credentials = MagicMock()
        mock_get_creds.return_value = mock_credentials
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        result = get_google_drive_api_service()

        mock_get_creds.assert_called_once()
        mock_build.assert_called_once_with("drive", "v3", credentials=mock_credentials)
        assert result == mock_service

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_uses_correct_api_version(self, mock_get_creds, mock_build):
        """Test that correct API version is used for Drive."""
        mock_credentials = MagicMock()
        mock_get_creds.return_value = mock_credentials

        get_google_drive_api_service()

        args, kwargs = mock_build.call_args
        assert args[0] == "drive"
        assert args[1] == "v3"

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_passes_credentials_to_build(self, mock_get_creds, mock_build):
        """Test that credentials are passed to build function."""
        mock_credentials = MagicMock()
        mock_get_creds.return_value = mock_credentials

        get_google_drive_api_service()

        args, kwargs = mock_build.call_args
        assert kwargs["credentials"] == mock_credentials
