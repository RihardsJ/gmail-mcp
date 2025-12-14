"""
Tests for format_email_for_display utility.
"""

import base64

from gmail_mcp_server.utils.format_email_for_display import format_email_for_display


class TestFormatEmailForDisplay:
    """Tests for format_email_for_display function."""

    def test_formats_complete_email(self, sample_email_message):
        """Test formatting a complete email message."""
        result = format_email_for_display(sample_email_message)

        assert "ID: msg123" in result
        assert "Thread ID: thread456" in result
        assert "From: sender@example.com" in result
        assert "Subject: Test Email" in result
        assert "Date: Mon, 01 Jan 2024 12:00:00 +0000" in result
        assert "Body:" in result
        assert "Hello, this is a test email." in result

    def test_formats_email_with_missing_headers(self):
        """Test formatting email with missing headers."""
        message = {
            "id": "msg999",
            "threadId": "thread999",
            "payload": {"headers": [], "body": {"data": ""}},
        }

        result = format_email_for_display(message)

        assert "ID: msg999" in result
        assert "Thread ID: thread999" in result
        assert "From: Unknown" in result
        assert "Subject: (No Subject)" in result
        assert "Date: Unknown" in result

    def test_formats_email_with_no_body(self):
        """Test formatting email with no body."""
        message = {
            "id": "msg123",
            "threadId": "thread123",
            "payload": {
                "headers": [
                    {"name": "From", "value": "test@example.com"},
                    {"name": "Subject", "value": "Test"},
                    {"name": "Date", "value": "Mon, 01 Jan 2024 12:00:00"},
                ],
                "body": {},
            },
        }

        result = format_email_for_display(message)

        assert "ID: msg123" in result
        assert "From: test@example.com" in result
        assert "Body:" in result

    def test_formats_multipart_email(self, sample_email_payload_multipart):
        """Test formatting multipart email message."""
        message = {
            "id": "msg_multipart",
            "threadId": "thread_multipart",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Multipart Test"},
                    {"name": "Date", "value": "Tue, 02 Jan 2024 10:00:00"},
                ],
                **sample_email_payload_multipart,
            },
        }

        result = format_email_for_display(message)

        assert "ID: msg_multipart" in result
        assert "From: sender@example.com" in result
        assert "Subject: Multipart Test" in result
        assert "Hello, this is plain text." in result

    def test_output_format_structure(self, sample_email_message):
        """Test that output follows expected structure."""
        result = format_email_for_display(sample_email_message)
        lines = result.split("\n")

        assert lines[0].startswith("ID:")
        assert lines[1].startswith("Thread ID:")
        assert lines[2].startswith("Date:")
        assert lines[3].startswith("From:")
        assert lines[4].startswith("Subject:")
        assert lines[5] == ""
        assert lines[6] == "Body:"

    def test_formats_email_with_unicode_subject(self):
        """Test formatting email with unicode characters in subject."""
        message = {
            "id": "msg_unicode",
            "threadId": "thread_unicode",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "测试主题 🎉"},
                    {"name": "Date", "value": "Wed, 03 Jan 2024 15:30:00"},
                ],
                "body": {
                    "data": base64.urlsafe_b64encode(
                        "Unicode body 你好".encode()
                    ).decode()
                },
            },
        }

        result = format_email_for_display(message)

        assert "Subject: 测试主题 🎉" in result
        assert "Unicode body 你好" in result

    def test_formats_email_with_complex_from_header(self):
        """Test formatting email with complex From header."""
        message = {
            "id": "msg_complex",
            "threadId": "thread_complex",
            "payload": {
                "headers": [
                    {"name": "From", "value": "John Doe <john.doe@example.com>"},
                    {"name": "Subject", "value": "Test"},
                    {"name": "Date", "value": "Thu, 04 Jan 2024 08:00:00"},
                ],
                "body": {"data": base64.urlsafe_b64encode(b"Test body").decode()},
            },
        }

        result = format_email_for_display(message)

        assert "From: John Doe <john.doe@example.com>" in result

    def test_formats_email_with_long_body(self):
        """Test formatting email with very long body."""
        long_body = "A" * 5000
        message = {
            "id": "msg_long",
            "threadId": "thread_long",
            "payload": {
                "headers": [
                    {"name": "From", "value": "sender@example.com"},
                    {"name": "Subject", "value": "Long Email"},
                    {"name": "Date", "value": "Fri, 05 Jan 2024 12:00:00"},
                ],
                "body": {"data": base64.urlsafe_b64encode(long_body.encode()).decode()},
            },
        }

        result = format_email_for_display(message)

        assert long_body in result
        assert "ID: msg_long" in result
