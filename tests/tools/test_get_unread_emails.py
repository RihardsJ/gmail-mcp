"""
Tests for get_unread_emails tool.
"""

import base64
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from googleapiclient.errors import HttpError

from gmail_mcp_server.tools.get_unread_emails import (
    GmailAPIError,
    _get_email_content,
    _list_all_email_content,
    get_unread_emails,
)


class TestGetUnreadEmails:
    """Tests for get_unread_emails function."""

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_retrieves_unread_emails_successfully(
        self, mock_get_service, mock_gmail_service
    ):
        """Test successfully retrieving unread emails."""
        mock_get_service.return_value = mock_gmail_service

        # Mock the messages list response
        mock_gmail_service.users().messages().list().execute.return_value = {
            "messages": [{"id": "msg1"}, {"id": "msg2"}]
        }

        # Mock individual message retrieval
        message_data = {
            "id": "msg1",
            "threadId": "thread1",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Test"},
                    {"name": "Date", "value": "Mon, 01 Jan 2024 12:00:00"},
                ],
                "body": {"data": base64.urlsafe_b64encode(b"Test body").decode()},
            },
        }

        mock_gmail_service.users().messages().get().execute.return_value = message_data

        results = await get_unread_emails(limit=2)

        assert len(results) == 2
        assert all(r.type == "text" for r in results)
        assert "From: sender@example.com" in results[0].text

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_returns_empty_list_when_no_unread_emails(
        self, mock_get_service, mock_gmail_service
    ):
        """Test returning empty list when no unread emails exist."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().messages().list().execute.return_value = {}

        results = await get_unread_emails(limit=5)

        assert results == []

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_respects_limit_parameter(self, mock_get_service, mock_gmail_service):
        """Test that limit parameter is respected."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().messages().list().execute.return_value = {}

        await get_unread_emails(limit=3)

        # Verify maxResults parameter is passed
        list_call = mock_gmail_service.users().messages().list
        list_call.assert_called_with(userId="me", labelIds=["UNREAD"], maxResults=3)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_handles_http_error(self, mock_get_service, mock_gmail_service):
        """Test handling of HttpError from Gmail API."""
        mock_get_service.return_value = mock_gmail_service

        # Create a proper HttpError
        http_error = HttpError(resp=Mock(status=403), content=b"Rate limit exceeded")
        mock_gmail_service.users().messages().list().execute.side_effect = http_error

        with pytest.raises(GmailAPIError) as exc_info:
            await get_unread_emails()

        assert "Gmail API Error" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_handles_unexpected_exception(
        self, mock_get_service, mock_gmail_service
    ):
        """Test handling of unexpected exceptions."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().messages().list().execute.side_effect = ValueError(
            "Unexpected error"
        )

        with pytest.raises(GmailAPIError) as exc_info:
            await get_unread_emails()

        assert "Unexpected Error retrieving unread emails" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_default_limit_is_five(self, mock_get_service, mock_gmail_service):
        """Test that default limit is 5."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().messages().list().execute.return_value = {}

        await get_unread_emails()

        list_call = mock_gmail_service.users().messages().list
        call_args = list_call.call_args
        assert call_args[1]["maxResults"] == 5

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.get_unread_emails.get_gmail_api_service")
    async def test_formats_multipart_emails(self, mock_get_service, mock_gmail_service):
        """Test formatting multipart emails."""
        mock_get_service.return_value = mock_gmail_service

        mock_gmail_service.users().messages().list().execute.return_value = {
            "messages": [{"id": "msg1"}]
        }

        multipart_message = {
            "id": "msg1",
            "threadId": "thread1",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Multipart"},
                    {"name": "Date", "value": "Mon, 01 Jan 2024 12:00:00"},
                ],
                "parts": [
                    {
                        "mimeType": "text/plain",
                        "body": {
                            "data": base64.urlsafe_b64encode(b"Plain text").decode()
                        },
                    }
                ],
            },
        }

        mock_gmail_service.users().messages().get().execute.return_value = (
            multipart_message
        )

        results = await get_unread_emails(limit=1)

        assert len(results) == 1
        assert "Plain text" in results[0].text


class TestGetEmailContent:
    """Tests for _get_email_content helper function."""

    @pytest.mark.asyncio
    async def test_retrieves_single_email(self, mock_gmail_service):
        """Test retrieving a single email."""
        message_data = {
            "id": "msg123",
            "threadId": "thread123",
            "payload": {"headers": []},
        }

        mock_gmail_service.users().messages().get().execute.return_value = message_data

        result = await _get_email_content(mock_gmail_service, "msg123")

        assert result == message_data
        # Verify the get method was called with correct parameters
        mock_gmail_service.users().messages().get.assert_called_with(
            userId="me", id="msg123"
        )


class TestListAllEmailContent:
    """Tests for _list_all_email_content helper function."""

    @pytest.mark.asyncio
    async def test_retrieves_multiple_emails_in_parallel(self, mock_gmail_service):
        """Test retrieving multiple emails in parallel."""
        messages = [
            {"id": "msg1", "threadId": "thread1", "payload": {"headers": []}},
            {"id": "msg2", "threadId": "thread2", "payload": {"headers": []}},
            {"id": "msg3", "threadId": "thread3", "payload": {"headers": []}},
        ]

        # Mock returns different message for each call
        mock_gmail_service.users().messages().get().execute.side_effect = messages

        message_ids = ["msg1", "msg2", "msg3"]
        results = await _list_all_email_content(mock_gmail_service, message_ids)

        assert len(results) == 3
        assert results == messages

    @pytest.mark.asyncio
    async def test_handles_empty_message_list(self, mock_gmail_service):
        """Test handling empty message list."""
        results = await _list_all_email_content(mock_gmail_service, [])

        assert results == []

    @pytest.mark.asyncio
    async def test_retrieves_single_email_in_list(self, mock_gmail_service):
        """Test retrieving a single email in a list."""
        message = {"id": "msg1", "threadId": "thread1", "payload": {"headers": []}}

        mock_gmail_service.users().messages().get().execute.return_value = message

        results = await _list_all_email_content(mock_gmail_service, ["msg1"])

        assert len(results) == 1
        assert results[0] == message


class TestGmailAPIError:
    """Tests for GmailAPIError exception."""

    def test_gmail_api_error_is_exception(self):
        """Test that GmailAPIError is an Exception."""
        assert issubclass(GmailAPIError, Exception)

    def test_gmail_api_error_can_be_raised(self):
        """Test that GmailAPIError can be raised with message."""
        with pytest.raises(GmailAPIError) as exc_info:
            raise GmailAPIError("Test error message")

        assert str(exc_info.value) == "Test error message"
