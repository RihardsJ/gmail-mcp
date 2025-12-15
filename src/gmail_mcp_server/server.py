#!/usr/bin/env python3

import re

import mcp.types as types
from mcp.server import Server
from pydantic import AnyUrl, FileUrl

from .configs import configs
from .prompts import draft_professional_reply, schedule_meeting_reply, suggest_template
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


@mcp_server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="draft_professional_reply",
            description="Generate professional email replies following the 7 Cs framework and your personal AI directive. Uses chain of thought and role prompting for consistent voice.",
            arguments=[
                types.PromptArgument(
                    name="thread_id",
                    description="The email thread ID to reply to",
                    required=True,
                ),
                types.PromptArgument(
                    name="key_points",
                    description="Key points to include in the reply",
                    required=False,
                ),
                types.PromptArgument(
                    name="tone",
                    description="Desired tone: formal, professional, or friendly",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name="schedule_meeting_reply",
            description="Draft meeting acceptance or proposal with calendar availability context. Automatically checks your calendar and proposes 2 time slots per your directive.",
            arguments=[
                types.PromptArgument(
                    name="thread_id",
                    description="The meeting request email thread ID",
                    required=True,
                ),
                types.PromptArgument(
                    name="date_range_start",
                    description="Start date for availability check (ISO format)",
                    required=True,
                ),
                types.PromptArgument(
                    name="date_range_end",
                    description="End date for availability check (ISO format)",
                    required=True,
                ),
                types.PromptArgument(
                    name="proposed_times",
                    description="Optional specific times to propose",
                    required=False,
                ),
            ],
        ),
        types.Prompt(
            name="suggest_template",
            description="Analyze an email and suggest the most appropriate personal template from your collection of 11 templates using few-shot learning.",
            arguments=[
                types.PromptArgument(
                    name="thread_id",
                    description="The email thread ID to analyze",
                    required=True,
                )
            ],
        ),
    ]


@mcp_server.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> types.GetPromptResult:
    if arguments is None:
        arguments = {}

    match name:
        case "draft_professional_reply":
            return await draft_professional_reply(arguments)
        case "schedule_meeting_reply":
            return await schedule_meeting_reply(arguments)
        case "suggest_template":
            return await suggest_template(arguments)

        case _:
            raise ValueError(f"Unknown prompt: {name}")
