#!/usr/bin/env python3
"""
Email threading header utilities for Gmail API.
"""

from typing import Optional


def build_threading_headers(
    message_id: Optional[str], references: Optional[str]
) -> dict[str, str]:
    """
    Build email threading headers (In-Reply-To and References).

    Args:
        message_id: Message-ID of the email being replied to
        references: Existing References header from original email

    Returns:
        Dictionary with 'In-Reply-To' and 'References' headers

    Example:
        >>> build_threading_headers("msg1", "msg0")
        {'In-Reply-To': 'msg1', 'References': 'msg0 msg1'}
    """
    if not message_id:
        return {}

    headers = {"In-Reply-To": message_id}

    # Build References header (previous references + current message)
    if references:
        headers["References"] = f"{references} {message_id}"
    else:
        headers["References"] = message_id

    return headers
