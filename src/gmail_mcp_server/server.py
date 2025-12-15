#!/usr/bin/env python3

import re

import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl, FileUrl

from .configs import configs
from .resources import get_calendar_availability, get_email_guidelines
from .tools import create_draft_reply, get_unread_emails
from .utils import format_to_rfc3339

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


@mcp_server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    return [
        types.Resource(
            uri=FileUrl("file:///7cs-communication.md"),
            name="7 Cs of Effective Communication",
            description="Professional email drafting guidelines based on the 7 Cs framework: Clear, Concise, Concrete, Correct, Coherent, Complete, and Courteous.",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri=FileUrl("file:///personal-templates.md"),
            name="Personal Email Templates",
            description="Collection of 11 essential email templates for everyday personal tasks like appointments, quotes, birthday wishes, and more.",
            mimeType="text/markdown",
        ),
        types.Resource(
            uri=FileUrl("file:///ai-drafting-directive.md"),
            name="AI Email Drafting Directive",
            description="Comprehensive directive for AI-assisted email drafting incorporating Dale Carnegie, Robert Cialdini, and Stephen Covey principles.",
            mimeType="text/markdown",
        ),
    ]


@mcp_server.list_resource_templates()
async def list_resource_templates() -> list[types.ResourceTemplate]:
    return [
        types.ResourceTemplate(
            uriTemplate="calendar:///availability/{startDateTime}/{endDateTime}",
            name="Calendar Availability",
            description="Availability information for a specific time range.",
            mimeType="application/json",
        ),
    ]


@mcp_server.read_resource()
async def handle_read_resource(
    uri: AnyUrl,
):
    uri_str = str(uri)

    # Resource templates cannot be matched closely, so check them first using regex
    calendar_pattern = r"calendar:///availability/([^/]+)/([^/]+)"
    calendar_match = re.match(calendar_pattern, uri_str)
    if calendar_match:
        return await get_calendar_availability(
            format_to_rfc3339(calendar_match.group(1)),
            format_to_rfc3339(calendar_match.group(2)),
        )

    # Check static resource urls using close comparison
    match uri_str:
        case "file:///7cs-communication.md":
            return await get_email_guidelines("7cs")
        case "file:///ai-drafting-directive.md":
            return await get_email_guidelines("directive")
        case "file:///personal-templates.md":
            return await get_email_guidelines("email_templates")
        case _:
            raise ValueError(f"Unknown resource: {uri_str}")
