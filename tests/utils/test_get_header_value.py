"""
Tests for get_header_value utility.
"""

from gmail_mcp_server.utils.get_header_value import get_header_value


class TestGetHeaderValue:
    """Tests for get_header_value function."""

    def test_get_existing_header(self):
        """Test retrieving an existing header value."""
        headers = [
            {"name": "From", "value": "sender@example.com"},
            {"name": "Subject", "value": "Test Subject"},
        ]
        result = get_header_value(headers, "From")
        assert result == "sender@example.com"

    def test_get_header_case_insensitive(self):
        """Test that header lookup is case-insensitive."""
        headers = [{"name": "Content-Type", "value": "text/html"}]
        assert get_header_value(headers, "content-type") == "text/html"
        assert get_header_value(headers, "CONTENT-TYPE") == "text/html"
        assert get_header_value(headers, "Content-Type") == "text/html"

    def test_get_nonexistent_header_returns_default(self):
        """Test that default value is returned for missing headers."""
        headers = [{"name": "From", "value": "sender@example.com"}]
        result = get_header_value(headers, "To", default="default@example.com")
        assert result == "default@example.com"

    def test_get_nonexistent_header_returns_none(self):
        """Test that None is returned when no default is provided."""
        headers = [{"name": "From", "value": "sender@example.com"}]
        result = get_header_value(headers, "To")
        assert result is None

    def test_empty_headers_list(self):
        """Test with empty headers list."""
        result = get_header_value([], "From", default="default")
        assert result == "default"

    def test_header_with_empty_value(self):
        """Test retrieving header with empty value."""
        headers = [{"name": "Subject", "value": ""}]
        result = get_header_value(headers, "Subject")
        assert result == ""

    def test_duplicate_headers_returns_first(self):
        """Test that first matching header is returned when duplicates exist."""
        headers = [
            {"name": "Received", "value": "first"},
            {"name": "Received", "value": "second"},
        ]
        result = get_header_value(headers, "Received")
        assert result == "first"

    def test_malformed_header_missing_name(self):
        """Test handling of malformed header without 'name' key."""
        headers = [
            {"value": "test@example.com"},
            {"name": "From", "value": "sender@example.com"},
        ]
        result = get_header_value(headers, "From")
        assert result == "sender@example.com"

    def test_malformed_header_missing_value(self):
        """Test handling of malformed header without 'value' key."""
        headers = [{"name": "From"}]
        result = get_header_value(headers, "From")
        assert result is None

    def test_header_with_special_characters(self):
        """Test header values containing special characters."""
        headers = [
            {
                "name": "From",
                "value": "Test User <test@example.com>",
            }
        ]
        result = get_header_value(headers, "From")
        assert result == "Test User <test@example.com>"

    def test_multiple_headers(self):
        """Test searching through multiple headers."""
        headers = [
            {"name": "From", "value": "sender@example.com"},
            {"name": "To", "value": "recipient@example.com"},
            {"name": "Subject", "value": "Test"},
            {"name": "Date", "value": "Mon, 01 Jan 2024 12:00:00"},
        ]
        assert get_header_value(headers, "From") == "sender@example.com"
        assert get_header_value(headers, "To") == "recipient@example.com"
        assert get_header_value(headers, "Subject") == "Test"
        assert get_header_value(headers, "Date") == "Mon, 01 Jan 2024 12:00:00"
