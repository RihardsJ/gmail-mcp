"""
Tests for ensure_reply_subject utility.
"""

import pytest

from gmail_mcp_server.utils.ensure_reply_subject import ensure_reply_subject


class TestEnsureReplySubject:
    """Tests for ensure_reply_subject function."""

    def test_adds_re_prefix_to_subject(self):
        """Test that 'Re: ' is added to subject without prefix."""
        result = ensure_reply_subject("Hello World")
        assert result == "Re: Hello World"

    def test_preserves_existing_re_prefix(self):
        """Test that existing 'Re: ' prefix is preserved."""
        result = ensure_reply_subject("Re: Hello World")
        assert result == "Re: Hello World"

    def test_case_insensitive_re_detection(self):
        """Test that 'RE:', 're:', 'Re:' are all recognized."""
        assert ensure_reply_subject("RE: Test") == "RE: Test"
        assert ensure_reply_subject("re: Test") == "re: Test"
        assert ensure_reply_subject("Re: Test") == "Re: Test"

    def test_empty_subject_returns_re_only(self):
        """Test that empty subject returns 'Re: '."""
        result = ensure_reply_subject("")
        assert result == "Re: "

    def test_none_subject_returns_re_only(self):
        """Test that None subject returns 'Re: '."""
        result = ensure_reply_subject(None)
        assert result == "Re: "

    def test_whitespace_only_subject(self):
        """Test subject with only whitespace."""
        result = ensure_reply_subject("   ")
        assert result == "Re:    "

    def test_subject_starting_with_re_but_no_colon(self):
        """Test that 'Re' without colon gets 'Re: ' prefix."""
        result = ensure_reply_subject("Regular Expression")
        assert result == "Re: Regular Expression"

    def test_re_in_middle_of_subject(self):
        """Test that 'Re:' in the middle doesn't prevent prefix."""
        result = ensure_reply_subject("FW: Re: Test")
        assert result == "Re: FW: Re: Test"

    def test_subject_with_special_characters(self):
        """Test subjects with special characters."""
        result = ensure_reply_subject("Meeting @ 3pm - Don't forget!")
        assert result == "Re: Meeting @ 3pm - Don't forget!"

    def test_subject_with_unicode(self):
        """Test subjects with unicode characters."""
        result = ensure_reply_subject("你好 世界")
        assert result == "Re: 你好 世界"

    def test_very_long_subject(self):
        """Test with very long subject line."""
        long_subject = "A" * 1000
        result = ensure_reply_subject(long_subject)
        assert result == f"Re: {long_subject}"

    def test_re_with_different_spacing(self):
        """Test 'Re:' detection with various spacing."""
        # Should preserve as-is since it starts with 're:'
        assert ensure_reply_subject("Re:Test") == "Re:Test"
        assert ensure_reply_subject("Re:  Test") == "Re:  Test"
