"""
Tests for Gmail API service module.
"""

from unittest.mock import MagicMock, Mock, mock_open, patch

from gmail_mcp_server.services.google_oauth_credentials import (
    get_google_oauth_credentials as get_gmail_oauth_credentials,
)
from gmail_mcp_server.services.google_workspace_service import get_gmail_api_service


class TestGetGmailOAuthCredentials:
    """Tests for get_gmail_oauth_credentials function."""

    @patch("gmail_mcp_server.services.google_oauth_credentials.os.path.exists")
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.Credentials.from_authorized_user_file"
    )
    def test_loads_existing_valid_credentials(
        self, mock_from_file, mock_exists, mock_credentials
    ):
        """Test loading existing valid credentials from file."""
        mock_exists.return_value = True
        mock_from_file.return_value = mock_credentials

        result = get_gmail_oauth_credentials()

        assert result == mock_credentials
        mock_from_file.assert_called_once()
        mock_exists.assert_called_once()

    @patch("gmail_mcp_server.services.google_oauth_credentials.os.path.exists")
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.Credentials.from_authorized_user_file"
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_refreshes_expired_credentials(
        self, mock_file, mock_from_file, mock_exists
    ):
        """Test refreshing expired credentials."""
        # Create expired credentials
        expired_creds = Mock()
        expired_creds.valid = False
        expired_creds.expired = True
        expired_creds.refresh_token = "refresh_token"
        expired_creds.to_json.return_value = '{"token": "refreshed"}'

        mock_exists.return_value = True
        mock_from_file.return_value = expired_creds

        with patch.object(expired_creds, "refresh") as mock_refresh:
            result = get_gmail_oauth_credentials()

            mock_refresh.assert_called_once()
            assert result == expired_creds
            mock_file.assert_called()

    @patch("gmail_mcp_server.services.google_oauth_credentials.os.path.exists")
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.InstalledAppFlow.from_client_secrets_file"
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_creates_new_credentials_when_none_exist(
        self, mock_file, mock_flow_constructor, mock_exists, mock_flow
    ):
        """Test creating new credentials when none exist."""
        mock_exists.return_value = False
        mock_flow_constructor.return_value = mock_flow
        new_creds = Mock()
        new_creds.to_json.return_value = '{"token": "new_token"}'
        mock_flow.run_local_server.return_value = new_creds

        result = get_gmail_oauth_credentials()

        assert result == new_creds
        mock_flow.run_local_server.assert_called_once()
        mock_file.assert_called()

    @patch("gmail_mcp_server.services.google_oauth_credentials.os.path.exists")
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.Credentials.from_authorized_user_file"
    )
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.InstalledAppFlow.from_client_secrets_file"
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_creates_new_credentials_when_invalid_and_no_refresh_token(
        self, mock_file, mock_flow_constructor, mock_from_file, mock_exists, mock_flow
    ):
        """Test creating new credentials when existing creds are invalid with no refresh token."""
        invalid_creds = Mock()
        invalid_creds.valid = False
        invalid_creds.expired = False
        invalid_creds.refresh_token = None

        mock_exists.return_value = True
        mock_from_file.return_value = invalid_creds
        mock_flow_constructor.return_value = mock_flow

        new_creds = Mock()
        new_creds.to_json.return_value = '{"token": "new_token"}'
        mock_flow.run_local_server.return_value = new_creds

        result = get_gmail_oauth_credentials()

        assert result == new_creds
        mock_flow.run_local_server.assert_called_once_with(
            port=8100,
            success_message="Successfully authorized! You can now close this window.",
        )

    @patch("gmail_mcp_server.services.google_oauth_credentials.os.path.exists")
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.Credentials.from_authorized_user_file"
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_saves_credentials_after_refresh(
        self, mock_file, mock_from_file, mock_exists
    ):
        """Test that credentials are saved after refresh."""
        expired_creds = Mock()
        expired_creds.valid = False
        expired_creds.expired = True
        expired_creds.refresh_token = "refresh_token"
        expired_creds.to_json.return_value = '{"token": "refreshed_token"}'

        mock_exists.return_value = True
        mock_from_file.return_value = expired_creds

        with patch.object(expired_creds, "refresh"):
            get_gmail_oauth_credentials()

            # Verify file was opened for writing
            mock_file.assert_called()
            # Verify credentials JSON was written
            handle = mock_file()
            handle.write.assert_called_with('{"token": "refreshed_token"}')

    @patch("gmail_mcp_server.services.google_oauth_credentials.os.path.exists")
    @patch(
        "gmail_mcp_server.services.google_oauth_credentials.InstalledAppFlow.from_client_secrets_file"
    )
    @patch("builtins.open", new_callable=mock_open)
    def test_saves_credentials_after_oauth_flow(
        self, mock_file, mock_flow_constructor, mock_exists, mock_flow
    ):
        """Test that credentials are saved after OAuth flow."""
        mock_exists.return_value = False
        mock_flow_constructor.return_value = mock_flow

        new_creds = Mock()
        new_creds.to_json.return_value = '{"token": "oauth_token"}'
        mock_flow.run_local_server.return_value = new_creds

        get_gmail_oauth_credentials()

        # Verify credentials were saved
        handle = mock_file()
        handle.write.assert_called_with('{"token": "oauth_token"}')


class TestGetGmailApiService:
    """Tests for get_gmail_api_service function."""

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_builds_gmail_service(self, mock_get_creds, mock_build, mock_credentials):
        """Test building Gmail API service."""
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
    def test_uses_correct_api_version(
        self, mock_get_creds, mock_build, mock_credentials
    ):
        """Test that correct API version is used."""
        mock_get_creds.return_value = mock_credentials

        get_gmail_api_service()

        args, kwargs = mock_build.call_args
        assert args[0] == "gmail"
        assert args[1] == "v1"

    @patch("gmail_mcp_server.services.google_workspace_service.build")
    @patch(
        "gmail_mcp_server.services.google_workspace_service.get_google_oauth_credentials"
    )
    def test_passes_credentials_to_build(
        self, mock_get_creds, mock_build, mock_credentials
    ):
        """Test that credentials are passed to build function."""
        mock_get_creds.return_value = mock_credentials

        get_gmail_api_service()

        args, kwargs = mock_build.call_args
        assert kwargs["credentials"] == mock_credentials
