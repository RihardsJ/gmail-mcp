#!/usr/bin/env python3
"""
Email body extraction utilities for Gmail API messages.
"""

import base64
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def get_email_body(payload: dict) -> str:
    """
    Extract email body from message payload.

    This function handles both simple and multipart email messages,
    preferring text/plain over text/html content.

    Args:
        payload: Gmail API message payload dictionary

    Returns:
        Decoded email body text, or empty string if no body found

    Example:
        >>> payload = {"body": {"data": "SGVsbG8gV29ybGQ="}}
        >>> get_email_body(payload)
        'Hello World'
    """

    def _decode_base64(data: str) -> str:
        """Decode base64 urlsafe encoded string"""
        try:
            return base64.urlsafe_b64decode(data).decode("utf-8")
        except Exception as e:
            logger.warning(f"Failed to decode base64 data: {e}")
            return ""

    def _extract_text_from_parts(parts: list[dict]) -> Optional[str]:
        """
        Recursively extract text from email parts.

        Prefers text/plain over text/html content.
        """
        text_plain = None
        text_html = None

        for part in parts:
            mime_type = part.get("mimeType", "")

            # Recursively check nested parts first
            if "parts" in part:
                nested_text = _extract_text_from_parts(part["parts"])
                if nested_text:
                    return nested_text

            # Collect text/plain content
            if mime_type == "text/plain" and "data" in part.get("body", {}):
                text_plain = _decode_base64(part["body"]["data"])
                if text_plain:
                    return text_plain

            # Collect text/html as fallback
            if mime_type == "text/html" and "data" in part.get("body", {}):
                if not text_html:
                    text_html = _decode_base64(part["body"]["data"])

        return text_plain or text_html

    # Handle multipart messages
    if "parts" in payload:
        text = _extract_text_from_parts(payload["parts"])
        if text:
            return text

    # Handle simple messages
    if "body" in payload and "data" in payload["body"]:
        return _decode_base64(payload["body"]["data"])

    logger.warning("No email body found in payload")
    return ""
