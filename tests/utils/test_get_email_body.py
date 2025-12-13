"""
Tests for get_email_body utility.
"""

import base64

import pytest

from gmail_mcp_server.utils.get_email_body import get_email_body


class TestGetEmailBody:
    """Tests for get_email_body function."""

    def test_simple_text_plain_body(self):
        """Test extracting body from simple text/plain message."""
        body_text = "Hello, this is a test email."
        encoded = base64.urlsafe_b64encode(body_text.encode()).decode()
        payload = {"body": {"data": encoded}}

        result = get_email_body(payload)
        assert result == body_text

    def test_multipart_prefers_text_plain(self):
        """Test that text/plain is preferred over text/html in multipart messages."""
        text_plain = "Plain text version"
        text_html = "<html><body>HTML version</body></html>"

        payload = {
            "parts": [
                {
                    "mimeType": "text/html",
                    "body": {
                        "data": base64.urlsafe_b64encode(text_html.encode()).decode()
                    },
                },
                {
                    "mimeType": "text/plain",
                    "body": {
                        "data": base64.urlsafe_b64encode(text_plain.encode()).decode()
                    },
                },
            ]
        }

        result = get_email_body(payload)
        assert result == text_plain

    def test_multipart_falls_back_to_html(self):
        """Test that text/html is used when text/plain is not available."""
        text_html = "<html><body>HTML only</body></html>"

        payload = {
            "parts": [
                {
                    "mimeType": "text/html",
                    "body": {
                        "data": base64.urlsafe_b64encode(text_html.encode()).decode()
                    },
                }
            ]
        }

        result = get_email_body(payload)
        assert result == text_html

    def test_nested_multipart_parts(self):
        """Test extracting body from nested multipart structure."""
        text_plain = "Nested plain text"

        payload = {
            "parts": [
                {
                    "mimeType": "multipart/alternative",
                    "parts": [
                        {
                            "mimeType": "text/plain",
                            "body": {
                                "data": base64.urlsafe_b64encode(
                                    text_plain.encode()
                                ).decode()
                            },
                        }
                    ],
                }
            ]
        }

        result = get_email_body(payload)
        assert result == text_plain

    def test_empty_body_data(self):
        """Test handling of empty body data."""
        payload = {"body": {"data": ""}}
        result = get_email_body(payload)
        assert result == ""

    def test_no_body_field(self):
        """Test handling when no body field exists."""
        payload = {}
        result = get_email_body(payload)
        assert result == ""

    def test_multipart_with_no_text_parts(self):
        """Test multipart message with no text parts."""
        payload = {
            "parts": [
                {"mimeType": "image/png", "body": {}},
                {"mimeType": "application/pdf", "body": {}},
            ]
        }
        result = get_email_body(payload)
        assert result == ""

    def test_multipart_with_empty_parts(self):
        """Test multipart message with empty parts list."""
        payload = {"parts": []}
        result = get_email_body(payload)
        assert result == ""

    def test_unicode_characters_in_body(self):
        """Test body containing unicode characters."""
        body_text = "Hello 世界! 你好 🌍"
        encoded = base64.urlsafe_b64encode(body_text.encode()).decode()
        payload = {"body": {"data": encoded}}

        result = get_email_body(payload)
        assert result == body_text

    def test_invalid_base64_data(self):
        """Test handling of invalid base64 data."""
        payload = {"body": {"data": "not-valid-base64!!!"}}
        result = get_email_body(payload)
        assert result == ""

    def test_multipart_attachment_with_text(self):
        """Test multipart message with both text and attachment."""
        text_plain = "Email body text"

        payload = {
            "parts": [
                {
                    "mimeType": "text/plain",
                    "body": {
                        "data": base64.urlsafe_b64encode(text_plain.encode()).decode()
                    },
                },
                {
                    "mimeType": "application/pdf",
                    "filename": "document.pdf",
                    "body": {"attachmentId": "abc123"},
                },
            ]
        }

        result = get_email_body(payload)
        assert result == text_plain

    def test_body_with_no_data_field(self):
        """Test body dictionary without 'data' field."""
        payload = {"body": {}}
        result = get_email_body(payload)
        assert result == ""

    def test_deeply_nested_multipart(self):
        """Test deeply nested multipart structure."""
        text_plain = "Deep nested text"

        payload = {
            "parts": [
                {
                    "mimeType": "multipart/mixed",
                    "parts": [
                        {
                            "mimeType": "multipart/alternative",
                            "parts": [
                                {
                                    "mimeType": "text/plain",
                                    "body": {
                                        "data": base64.urlsafe_b64encode(
                                            text_plain.encode()
                                        ).decode()
                                    },
                                }
                            ],
                        }
                    ],
                }
            ]
        }

        result = get_email_body(payload)
        assert result == text_plain

    def test_large_email_body(self):
        """Test with a large email body."""
        body_text = "A" * 10000
        encoded = base64.urlsafe_b64encode(body_text.encode()).decode()
        payload = {"body": {"data": encoded}}

        result = get_email_body(payload)
        assert result == body_text

    def test_multipart_text_plain_without_body_data(self):
        """Test multipart with text/plain part but no body data."""
        text_html = "<html>Fallback HTML</html>"

        payload = {
            "parts": [
                {"mimeType": "text/plain", "body": {}},
                {
                    "mimeType": "text/html",
                    "body": {
                        "data": base64.urlsafe_b64encode(text_html.encode()).decode()
                    },
                },
            ]
        }

        result = get_email_body(payload)
        assert result == text_html

    def test_urlsafe_base64_padding(self):
        """Test base64 decoding with and without padding."""
        body_text = "Test"
        encoded = base64.urlsafe_b64encode(body_text.encode()).decode()
        payload = {"body": {"data": encoded}}

        result = get_email_body(payload)
        assert result == body_text
