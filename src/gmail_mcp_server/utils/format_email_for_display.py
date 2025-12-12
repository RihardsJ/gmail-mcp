#!/usr/bin/env python3
"""
Email formatting utilities for displaying Gmail messages.
"""

from .get_email_body import get_email_body
from .get_header_value import get_header_value


def format_email_for_display(message: dict) -> str:
    """
    Format a Gmail API message for human-readable display.

    Args:
        message: Gmail API message object with 'id', 'threadId', 'payload', etc.

    Returns:
        Formatted string containing email metadata and body

    Example:
        >>> message = {
        ...     "id": "msg123",
        ...     "threadId": "thread456",
        ...     "payload": {"headers": [...]}
        ... }
        >>> print(format_email_for_display(message))
        ID: msg123
        Thread ID: thread456
        ...
    """
    headers = message["payload"]["headers"]

    sender = get_header_value(headers, "from", "Unknown")
    subject = get_header_value(headers, "subject", "(No Subject)")
    date = get_header_value(headers, "date", "Unknown")
    body = get_email_body(message["payload"])

    return (
        f"ID: {message['id']}\n"
        f"Thread ID: {message['threadId']}\n"
        f"Date: {date}\n"
        f"From: {sender}\n"
        f"Subject: {subject}\n"
        f"\nBody:\n{body}\n"
    )
