#!/usr/bin/env python3
"""
Gmail email utilities package.

This package provides common utilities for working with Gmail API messages,
including header extraction, body parsing, message formatting, and threading.
"""

from .build_threading_headers import build_threading_headers
from .ensure_reply_subject import ensure_reply_subject
from .format_email_for_display import format_email_for_display
from .get_email_body import get_email_body
from .get_header_value import get_header_value

__all__ = [
    "build_threading_headers",
    "ensure_reply_subject",
    "format_email_for_display",
    "get_email_body",
    "get_header_value",
]
