"""
Tests for build_threading_headers utility.
"""

import pytest

from gmail_mcp_server.utils.build_threading_headers import build_threading_headers


class TestBuildThreadingHeaders:
    """Tests for build_threading_headers function."""

    def test_creates_headers_with_message_id_and_references(self):
        """Test creating threading headers with both message_id and references."""
        result = build_threading_headers(
            message_id="<msg2@example.com>",
            references="<msg0@example.com> <msg1@example.com>",
        )
        assert result == {
            "In-Reply-To": "<msg2@example.com>",
            "References": "<msg0@example.com> <msg1@example.com> <msg2@example.com>",
        }

    def test_creates_headers_with_message_id_only(self):
        """Test creating threading headers with only message_id (no references)."""
        result = build_threading_headers(
            message_id="<msg1@example.com>", references=None
        )
        assert result == {
            "In-Reply-To": "<msg1@example.com>",
            "References": "<msg1@example.com>",
        }

    def test_creates_headers_with_empty_references(self):
        """Test creating threading headers with empty string references."""
        result = build_threading_headers(message_id="<msg1@example.com>", references="")
        assert result == {
            "In-Reply-To": "<msg1@example.com>",
            "References": "<msg1@example.com>",
        }

    def test_returns_empty_dict_when_message_id_is_none(self):
        """Test that empty dict is returned when message_id is None."""
        result = build_threading_headers(
            message_id=None, references="<msg0@example.com>"
        )
        assert result == {}

    def test_returns_empty_dict_when_message_id_is_empty(self):
        """Test that empty dict is returned when message_id is empty string."""
        result = build_threading_headers(message_id="", references="<msg0@example.com>")
        assert result == {}

    def test_single_reference_message(self):
        """Test with a single reference message."""
        result = build_threading_headers(
            message_id="<msg2@example.com>", references="<msg1@example.com>"
        )
        assert result == {
            "In-Reply-To": "<msg2@example.com>",
            "References": "<msg1@example.com> <msg2@example.com>",
        }

    def test_long_reference_chain(self):
        """Test with a long chain of references."""
        references = " ".join([f"<msg{i}@example.com>" for i in range(10)])
        result = build_threading_headers(
            message_id="<msg10@example.com>", references=references
        )
        assert result["In-Reply-To"] == "<msg10@example.com>"
        assert result["References"] == f"{references} <msg10@example.com>"

    def test_message_id_without_angle_brackets(self):
        """Test with message IDs that don't have angle brackets."""
        result = build_threading_headers(message_id="msg1", references="msg0")
        assert result == {
            "In-Reply-To": "msg1",
            "References": "msg0 msg1",
        }

    def test_message_id_with_special_characters(self):
        """Test message IDs with special characters."""
        result = build_threading_headers(
            message_id="<msg.1+test@example.com>",
            references="<msg.0+test@example.com>",
        )
        assert result == {
            "In-Reply-To": "<msg.1+test@example.com>",
            "References": "<msg.0+test@example.com> <msg.1+test@example.com>",
        }

    def test_none_message_id_with_none_references(self):
        """Test with both parameters as None."""
        result = build_threading_headers(message_id=None, references=None)
        assert result == {}

    def test_whitespace_only_message_id(self):
        """Test with whitespace-only message_id."""
        result = build_threading_headers(
            message_id="   ", references="<msg0@example.com>"
        )
        assert result == {
            "In-Reply-To": "   ",
            "References": "<msg0@example.com>    ",
        }
