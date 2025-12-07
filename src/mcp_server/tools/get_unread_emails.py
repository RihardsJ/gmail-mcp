#!/usr/bin/env python3

import mcp.types as types

__all__ = ["get_unread_emails"]


async def get_unread_emails(limit: int) -> list[types.TextContent]:
    """
    This MCP tool retrieves unread emails from Gmail.

    parameters:
        limit (int): The maximum number of unread emails to retrieve.

    returns:
        list[types.TextContent]: A list containing text content with the unread emails.

    example:
        await get_unread_emails(5)
    """
    # TODO: Implement actual Gmail API integration
    # For now, return a placeholder response

    return [
        types.TextContent(
            type="text",
            text=f"Retrieved up to {limit} unread emails (implementation pending)",
        )
    ]
