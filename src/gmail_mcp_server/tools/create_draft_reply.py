#!/usr/bin/env python3

import base64
import logging
from email.mime.text import MIMEText
from typing import TypedDict

import mcp.types as types
from googleapiclient.errors import HttpError

from ..configs import configs
from ..services.gmail_api_service import get_gmail_api_service

email_user = configs.get("email_user")
logger = logging.getLogger(__name__)


class ReplyArgs(TypedDict):
    thread_id: str
    reply_body: str


def _validate_arguments(arguments: dict) -> ReplyArgs:
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


async def create_draft_reply(arguments: dict) -> list[types.TextContent]:
    """
    This MCP tool creates a draft reply for an email.

    parameters:
        arguments (dict): A dictionary containing the 'thread_id': str and 'reply_body': str.

    returns:
        list[types.TextContent]: A list containing a text content object indicating the success or failure of the operation.

    example:
        await create_draft_reply({"thread_id": "1234567890", "reply_body": "Hello, world!"})

    Reference: https://developers.google.com/gmail/api/guides/drafts
    """

    validated_args = _validate_arguments(arguments)
    thread_id = validated_args["thread_id"]
    reply_body = validated_args["reply_body"]

    try:
        logger.debug("Initializing Gmail API service")
        gmail_service = get_gmail_api_service()

        # Get the original thread to extract necessary headers for proper threading
        logger.info(f"Retrieving thread {thread_id} to get original message details")
        thread = (
            gmail_service.users().threads().get(userId="me", id=thread_id).execute()
        )

        if not thread or "messages" not in thread or len(thread["messages"]) == 0:
            raise ValueError(f"Thread {thread_id} not found or has no messages")

        # Get the first message in the thread to extract headers
        original_message = thread["messages"][0]
        headers = original_message["payload"]["headers"]

        # Extract necessary headers for threading
        subject = next(
            (
                header["value"]
                for header in headers
                if header["name"].lower() == "subject"
            ),
            "",
        )
        message_id = next(
            (
                header["value"]
                for header in headers
                if header["name"].lower() == "message-id"
            ),
            None,
        )
        references = next(
            (
                header["value"]
                for header in headers
                if header["name"].lower() == "references"
            ),
            None,
        )

        # Ensure subject has "Re: " prefix if not already present
        if not subject.lower().startswith("re:"):
            subject = f"Re: {subject}"

        # Create the MIME message
        message = MIMEText(reply_body)
        message["to"] = next(
            (header["value"] for header in headers if header["name"].lower() == "from"),
            "",
        )
        message["subject"] = subject

        # Add threading headers
        if message_id:
            message["In-Reply-To"] = message_id
            # Build References header (includes previous references + the message we're replying to)
            if references:
                message["References"] = f"{references} {message_id}"
            else:
                message["References"] = message_id

        # Encode the message
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        # Create the draft with threading
        draft_body = {"message": {"raw": raw_message, "threadId": thread_id}}

        logger.info(f"Creating draft reply for thread {thread_id}")
        draft = (
            gmail_service.users()
            .drafts()
            .create(userId="me", body=draft_body)
            .execute()
        )

        draft_id = draft.get("id")
        logger.info(f"Draft created successfully with ID: {draft_id}")

        return [
            types.TextContent(
                type="text",
                text=f"Draft reply created successfully!\n\nDraft ID: {draft_id}\nThread ID: {thread_id}\nSubject: {subject}\n\nYou can find this draft in your Gmail drafts folder.",
            )
        ]

    except HttpError as e:
        error_msg = f"Gmail API Error: {str(e)}"
        logger.error(error_msg)
        return [
            types.TextContent(
                type="text",
                text=f"Error creating draft reply: {error_msg}",
            )
        ]
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg)
        return [
            types.TextContent(
                type="text",
                text=f"Error creating draft reply: {error_msg}",
            )
        ]
