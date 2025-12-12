#!/usr/bin/env python3
"""
Header extraction utilities for Gmail API messages.
"""

from typing import Optional


def get_header_value(
    headers: list[dict], header_name: str, default: Optional[str] = None
) -> Optional[str]:
    """
    Extract a header value from email headers by name.

    Args:
        headers: List of email header dictionaries with 'name' and 'value' keys
        header_name: Name of the header to extract (case-insensitive)
        default: Default value if header not found

    Returns:
        Header value or default

    Example:
        >>> headers = [{"name": "From", "value": "user@example.com"}]
        >>> get_header_value(headers, "from")
        'user@example.com'
    """
    return next(
        (
            header.get("value")
            for header in headers
            if header.get("name", "").lower() == header_name.lower()
        ),
        default,
    )
