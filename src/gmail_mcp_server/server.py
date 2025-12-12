#!/usr/bin/env python3

import mcp.types as types
from mcp.server import Server

from .configs import configs
from .tools import create_draft_reply, get_unread_emails

mcp_server = Server(configs["server_name"])


@mcp_server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_unread_emails",
            description="Get unread emails",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "The maximum number of emails to retrieve",
                        "default": configs["max_email_limit"],
                    },
                },
            },
        ),
        types.Tool(
            name="create_draft_email",
            description="Create a draft email",
            inputSchema={
                "type": "object",
                "properties": {
                    "thread_id": {
                        "type": "string",
                        "description": "The ID of the email thread obtained from get_unread_emails",
                    },
                    "reply_body": {
                        "type": "string",
                        "description": "The body content of the email reply",
                    },
                },
                "required": ["thread_id", "reply_body"],
            },
        ),
    ]


@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    match name:
        case "get_unread_emails":
            return await get_unread_emails(
                arguments.get("limit", configs["max_email_limit"])
            )
        case "create_draft_email":
            return await create_draft_reply(arguments)
        case _:
            raise ValueError(f"Unknown tool: {name}")
