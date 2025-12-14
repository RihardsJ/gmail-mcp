"""
Tests for email guidelines resources module.
"""

from unittest.mock import Mock, patch

import pytest

from gmail_mcp_server.resources.email_guidelines import (
    GoogleDriveAPIError,
    get_email_guidelines,
)


class TestGetEmailGuidelines:
    """Tests for get_email_guidelines function."""

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.resources.email_guidelines.get_google_drive_api_service")
    @patch("gmail_mcp_server.resources.email_guidelines.configs")
    async def test_retrieves_guideline_successfully(
        self, mock_configs, mock_get_service
    ):
        """Test successful retrieval of email guideline."""
        # Setup
        mock_configs.get.return_value = "test_doc_id_123"
        mock_service = Mock()
        mock_export = Mock()
        mock_export.execute.return_value = b"# Test Guideline\n\nContent here"
        mock_service.files().export.return_value = mock_export
        mock_get_service.return_value = mock_service

        # Execute
        result = await get_email_guidelines("7cs")

        # Verify
        assert result == b"# Test Guideline\n\nContent here"
        mock_configs.get.assert_called_once_with("google_docs.7cs_doc_id")
        mock_service.files().export.assert_called_once_with(
            fileId="test_doc_id_123", mimeType="text/markdown"
        )

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.resources.email_guidelines.configs")
    async def test_raises_error_for_invalid_guideline_name(self, mock_configs):
        """Test that invalid guideline name raises error."""
        with pytest.raises(GoogleDriveAPIError, match="Invalid guideline name"):
            await get_email_guidelines("invalid_name")

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.resources.email_guidelines.configs")
    async def test_raises_error_when_doc_id_not_found(self, mock_configs):
        """Test error when document ID is not in config."""
        mock_configs.get.return_value = None

        with pytest.raises(GoogleDriveAPIError, match="No document ID found"):
            await get_email_guidelines("7cs")

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.resources.email_guidelines.get_google_drive_api_service")
    @patch("gmail_mcp_server.resources.email_guidelines.configs")
    async def test_handles_http_error(self, mock_configs, mock_get_service):
        """Test handling of HTTP errors from Google Drive API."""
        from googleapiclient.errors import HttpError

        mock_configs.get.return_value = "test_doc_id"
        mock_service = Mock()
        mock_service.files().export().execute.side_effect = HttpError(
            resp=Mock(status=404), content=b"Not found"
        )
        mock_get_service.return_value = mock_service

        with pytest.raises(GoogleDriveAPIError, match="Google Drive API Error"):
            await get_email_guidelines("7cs")

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.resources.email_guidelines.get_google_drive_api_service")
    @patch("gmail_mcp_server.resources.email_guidelines.configs")
    async def test_all_valid_guideline_names(self, mock_configs, mock_get_service):
        """Test that all valid guideline names work."""
        mock_configs.get.return_value = "test_doc_id"
        mock_service = Mock()
        mock_export = Mock()
        mock_export.execute.return_value = b"# Test Content"
        mock_service.files().export.return_value = mock_export
        mock_get_service.return_value = mock_service

        valid_names = ["7cs", "email_templates", "directive"]

        for name in valid_names:
            result = await get_email_guidelines(name)
            assert result == b"# Test Content"
            mock_configs.get.assert_called_with(f"google_docs.{name}_doc_id")

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.resources.email_guidelines.get_google_drive_api_service")
    @patch("gmail_mcp_server.resources.email_guidelines.configs")
    async def test_exports_with_correct_mime_type(self, mock_configs, mock_get_service):
        """Test that export is called with text/markdown mime type."""
        mock_configs.get.return_value = "test_doc_id"
        mock_service = Mock()
        mock_export = Mock()
        mock_export.execute.return_value = b"content"
        mock_service.files().export.return_value = mock_export
        mock_get_service.return_value = mock_service

        await get_email_guidelines("7cs")

        # Verify the export was called with correct parameters
        mock_service.files().export.assert_called_with(
            fileId="test_doc_id", mimeType="text/markdown"
        )
