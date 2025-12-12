#!/usr/bin/env python3
"""
Email subject line utilities for replies.
"""

from typing import Optional


def ensure_reply_subject(subject: Optional[str]) -> str:
    """
    Ensure subject line has 'Re: ' prefix for replies.

    Args:
        subject: Original email subject

    Returns:
        Subject with 'Re: ' prefix if not already present

    Example:
        >>> ensure_reply_subject("Hello")
        'Re: Hello'
        >>> ensure_reply_subject("Re: Hello")
        'Re: Hello'
    """
    if not subject:
        return "Re: "

    if not subject.lower().startswith("re:"):
        return f"Re: {subject}"

    return subject
