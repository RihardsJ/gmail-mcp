#!/usr/bin/env python3

from typing import TypedDict

import mcp.types as types

from ..configs import configs

email_user = configs.get("email_user")


class ReplyArgs(TypedDict):
    thread_id: str
    reply_body: str


def validate_arguments(arguments: dict) -> ReplyArgs:
    """
    Helper function to validate arguments for create_draft_reply.
    """
    thread_id = arguments.get("thread_id")
    reply_body = arguments.get("reply_body")

    if not thread_id:
        raise ValueError(
            "Missing thread_id argument",
        )
    elif not reply_body:
        raise ValueError(
            "Missing reply_body argument",
        )
    else:
        return {"thread_id": thread_id, "reply_body": reply_body}


__all__ = ["create_draft_reply"]


async def create_draft_reply(arguments: dict) -> list[types.TextContent]:
    """
    This MCP tool creates a draft reply for an email.

    parameters:
        arguments (dict): A dictionary containing the 'thread_id': str and 'reply_body': str.

    returns:
        list[types.TextContent]: A list containing a text content object indicating the success or failure of the operation.

    example:
        await create_draft_reply({"thread_id": "1234567890", "reply_body": "Hello, world!"})
    """

    validated_args = validate_arguments(arguments)
    thread_id = validated_args["thread_id"]
    reply_body = validated_args["reply_body"]

    # TODO: Implement the logic to create correctly threaded draft reply

    return [
        types.TextContent(
            type="text",
            text=f"Draft reply created successfully for thread {thread_id} with body '{reply_body}'",
        )
    ]
