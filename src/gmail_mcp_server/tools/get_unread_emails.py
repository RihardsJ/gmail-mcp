#!/usr/bin/env python3

import asyncio
import logging

import mcp.types as types
from googleapiclient.errors import HttpError

from ..services.gmail_api_service import get_gmail_api_service
from ..utils import format_email_for_display

logger = logging.getLogger(__name__)


class GmailAPIError(Exception):
    """Exception raised when there is an error with the Gmail API."""

    pass


async def get_unread_emails(limit: int = 5) -> list[types.TextContent]:
    """
    Retrieves unread emails from Gmail.

    Reference: https://developers.google.com/workspace/explore?filter=&discoveryUrl=https%3A%2F%2Fgmail.googleapis.com%2F%24discovery%2Frest%3Fversion%3Dv1&discoveryRef=

    parameters:
        limit (int): The maximum number of unread emails to retrieve.

    returns:
        list[types.TextContent]: A list containing text content with the unread emails.

    example:
        await get_unread_emails(5)
    """

    try:
        logger.debug("Initializing Gmail API service")
        gmail_service = get_gmail_api_service()
        # Retrieve unread emails using the Gmail API service
        logger.info(f"Retrieving up to {limit} unread emails")
        unread_email_data = (
            gmail_service.users()
            .messages()
            .list(userId="me", labelIds=["UNREAD"], maxResults=limit)
            .execute()
        )
        message_ids = unread_email_data.get("messages", [])

        if not message_ids:
            logger.warning("No unread emails found")
            return []

        messages = await _list_all_email_content(
            gmail_service, [message_id["id"] for message_id in message_ids]
        )

        results = []
        for msg in messages:
            email_text = format_email_for_display(msg)
            results.append(types.TextContent(type="text", text=email_text))

        return results

    except HttpError as e:
        errMessage = f"Gmail API Error: {str(e)}"
        logger.error(errMessage)
        raise GmailAPIError(errMessage)
    except Exception as e:
        logger.error(f"Unexpected Error retrieving unread emails: {str(e)}")
        raise GmailAPIError(f"Unexpected Error retrieving unread emails: {str(e)}")


async def _get_email_content(gmail_service, message_id):
    """Async wrapper for Gmail API call"""
    logger.info(f"Retrieving email data for message ID: {message_id}")
    email_data = (
        gmail_service.users().messages().get(userId="me", id=message_id).execute()
    )
    return email_data


async def _list_all_email_content(gmail_service, message_ids):
    """Retrieve email data for a list of message IDs in parallel"""
    tasks = [
        _get_email_content(gmail_service, message_id) for message_id in message_ids
    ]
    email_data_list = await asyncio.gather(*tasks)
    return email_data_list
