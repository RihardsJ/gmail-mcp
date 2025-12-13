"""
Tests for create_draft_reply tool.
"""

import base64
from email.mime.text import MIMEText
from unittest.mock import MagicMock, Mock, patch

import pytest
from googleapiclient.errors import HttpError

from gmail_mcp_server.tools.create_draft_reply import (
    _validate_arguments,
    create_draft_reply,
)


class TestCreateDraftReply:
    """Tests for create_draft_reply function."""

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_creates_draft_reply_successfully(
        self, mock_get_service, mock_gmail_service, sample_thread
    ):
        """Test successfully creating a draft reply."""
        mock_get_service.return_value = mock_gmail_service

        # Mock thread retrieval
        mock_gmail_service.users().threads().get().execute.return_value = sample_thread

        # Mock draft creation
        mock_gmail_service.users().drafts().create().execute.return_value = {
            "id": "draft123"
        }

        arguments = {"thread_id": "thread123", "reply_body": "This is my reply"}

        results = await create_draft_reply(arguments)

        assert len(results) == 1
        assert results[0].type == "text"
        assert "Draft reply created successfully" in results[0].text
        assert "draft123" in results[0].text

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_creates_draft_with_correct_threading_headers(
        self, mock_get_service, mock_gmail_service, sample_thread
    ):
        """Test that draft includes correct threading headers."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.return_value = sample_thread

        mock_create = mock_gmail_service.users().drafts().create
        mock_create().execute.return_value = {"id": "draft123"}

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        await create_draft_reply(arguments)

        # Get the draft body that was passed to create
        call_args = mock_create.call_args
        draft_body = call_args[1]["body"]

        # Decode the message to check headers
        raw_message = draft_body["message"]["raw"]
        decoded = base64.urlsafe_b64decode(raw_message).decode()

        assert "In-Reply-To: <msg123@example.com>" in decoded
        assert "References: <msg0@example.com> <msg123@example.com>" in decoded

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_adds_re_prefix_to_subject(
        self, mock_get_service, mock_gmail_service, sample_thread
    ):
        """Test that 'Re: ' prefix is added to subject."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.return_value = sample_thread

        mock_create = mock_gmail_service.users().drafts().create
        mock_create().execute.return_value = {"id": "draft123"}

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        await create_draft_reply(arguments)

        call_args = mock_create.call_args
        draft_body = call_args[1]["body"]
        raw_message = draft_body["message"]["raw"]
        decoded = base64.urlsafe_b64decode(raw_message).decode()

        # Check for subject with Re: prefix (case-insensitive for header name)
        decoded_lower = decoded.lower()
        assert "subject: re: test thread" in decoded_lower

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_sets_correct_recipient(
        self, mock_get_service, mock_gmail_service, sample_thread
    ):
        """Test that recipient is set to original sender."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.return_value = sample_thread

        mock_create = mock_gmail_service.users().drafts().create
        mock_create().execute.return_value = {"id": "draft123"}

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        await create_draft_reply(arguments)

        call_args = mock_create.call_args
        draft_body = call_args[1]["body"]
        raw_message = draft_body["message"]["raw"]
        decoded = base64.urlsafe_b64decode(raw_message).decode()

        # Check for recipient (case-insensitive for header name)
        decoded_lower = decoded.lower()
        assert "to: sender@example.com" in decoded_lower

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_includes_thread_id_in_draft(
        self, mock_get_service, mock_gmail_service, sample_thread
    ):
        """Test that thread ID is included in draft."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.return_value = sample_thread

        mock_create = mock_gmail_service.users().drafts().create
        mock_create().execute.return_value = {"id": "draft123"}

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        await create_draft_reply(arguments)

        call_args = mock_create.call_args
        draft_body = call_args[1]["body"]

        assert draft_body["message"]["threadId"] == "thread123"

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_handles_http_error(self, mock_get_service, mock_gmail_service):
        """Test handling of HttpError from Gmail API."""
        mock_get_service.return_value = mock_gmail_service

        http_error = HttpError(resp=Mock(status=403), content=b"Permission denied")
        mock_gmail_service.users().threads().get().execute.side_effect = http_error

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        results = await create_draft_reply(arguments)

        assert len(results) == 1
        assert "Error creating draft reply" in results[0].text
        assert "Gmail API Error" in results[0].text

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_handles_missing_thread(self, mock_get_service, mock_gmail_service):
        """Test handling when thread is not found."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.return_value = {}

        arguments = {"thread_id": "nonexistent", "reply_body": "Reply"}

        results = await create_draft_reply(arguments)

        assert len(results) == 1
        assert "Error creating draft reply" in results[0].text

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_handles_thread_with_no_messages(
        self, mock_get_service, mock_gmail_service
    ):
        """Test handling thread with no messages."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.return_value = {
            "id": "thread123",
            "messages": [],
        }

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        results = await create_draft_reply(arguments)

        assert len(results) == 1
        assert "Error creating draft reply" in results[0].text

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.tools.create_draft_reply.get_gmail_api_service")
    async def test_handles_unexpected_exception(
        self, mock_get_service, mock_gmail_service
    ):
        """Test handling of unexpected exceptions."""
        mock_get_service.return_value = mock_gmail_service
        mock_gmail_service.users().threads().get().execute.side_effect = RuntimeError(
            "Unexpected error"
        )

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}

        results = await create_draft_reply(arguments)

        assert len(results) == 1
        assert "Error creating draft reply" in results[0].text
        assert "Unexpected error" in results[0].text

    @pytest.mark.asyncio
    async def test_validates_arguments(self):
        """Test that arguments are validated."""
        # Missing thread_id
        with pytest.raises(ValueError) as exc_info:
            await create_draft_reply({"reply_body": "Reply"})
        assert "Missing thread_id" in str(exc_info.value)

        # Missing reply_body
        with pytest.raises(ValueError) as exc_info:
            await create_draft_reply({"thread_id": "thread123"})
        assert "Missing reply_body" in str(exc_info.value)


class TestValidateArguments:
    """Tests for _validate_arguments helper function."""

    def test_validates_correct_arguments(self):
        """Test validation of correct arguments."""
        args = {"thread_id": "thread123", "reply_body": "Reply text"}
        result = _validate_arguments(args)

        assert result["thread_id"] == "thread123"
        assert result["reply_body"] == "Reply text"

    def test_raises_error_for_missing_thread_id(self):
        """Test that error is raised for missing thread_id."""
        args = {"reply_body": "Reply text"}

        with pytest.raises(ValueError) as exc_info:
            _validate_arguments(args)

        assert "Missing thread_id argument" in str(exc_info.value)

    def test_raises_error_for_missing_reply_body(self):
        """Test that error is raised for missing reply_body."""
        args = {"thread_id": "thread123"}

        with pytest.raises(ValueError) as exc_info:
            _validate_arguments(args)

        assert "Missing reply_body argument" in str(exc_info.value)

    def test_raises_error_for_empty_thread_id(self):
        """Test that error is raised for empty thread_id."""
        args = {"thread_id": "", "reply_body": "Reply"}

        with pytest.raises(ValueError) as exc_info:
            _validate_arguments(args)

        assert "Missing thread_id argument" in str(exc_info.value)

    def test_raises_error_for_empty_reply_body(self):
        """Test that error is raised for empty reply_body."""
        args = {"thread_id": "thread123", "reply_body": ""}

        with pytest.raises(ValueError) as exc_info:
            _validate_arguments(args)

        assert "Missing reply_body argument" in str(exc_info.value)

    def test_raises_error_for_none_values(self):
        """Test that error is raised for None values."""
        with pytest.raises(ValueError):
            _validate_arguments({"thread_id": None, "reply_body": "Reply"})

        with pytest.raises(ValueError):
            _validate_arguments({"thread_id": "thread123", "reply_body": None})

    def test_accepts_whitespace_in_reply_body(self):
        """Test that whitespace-only reply body is accepted."""
        args = {"thread_id": "thread123", "reply_body": "   "}
        result = _validate_arguments(args)

        assert result["reply_body"] == "   "
