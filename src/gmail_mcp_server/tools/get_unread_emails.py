#!/usr/bin/env python3

import asyncio
import base64
import logging

import mcp.types as types
from googleapiclient.errors import HttpError

from ..services.gmail_api_service import get_gmail_api_service

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

        messages = await list_all_email_content(
            gmail_service, [message_id["id"] for message_id in message_ids]
        )

        results = []
        for msg in messages:
            headers = msg["payload"]["headers"]
            sender = next(
                (
                    header["value"]
                    for header in headers
                    if header["name"].lower() == "from"
                ),
                None,
            )
            subject = next(
                (
                    header["value"]
                    for header in headers
                    if header["name"].lower() == "subject"
                ),
                None,
            )
            date = next(
                (
                    header["value"]
                    for header in headers
                    if header["name"].lower() == "date"
                ),
                None,
            )

            body = _get_email_body(msg["payload"])

            email_text = f"ID: {msg['id']}\nThread ID: {msg['threadId']}\nDate: {date}\nFrom: {sender}\nSubject: {subject}\n\nBody:\n{body}\n"
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


async def list_all_email_content(gmail_service, message_ids):
    """Retrieve email data for a list of message IDs in parallel"""
    tasks = [
        _get_email_content(gmail_service, message_id) for message_id in message_ids
    ]
    email_data_list = await asyncio.gather(*tasks)
    return email_data_list


def _get_email_body(payload: dict) -> str:
    """
    Extract email body from message payload

    Args:
        payload (dict): Message payload

    Returns:
        str: Email body
    """

    def extract_text_from_parts(parts):
        """Recursively extract text from email parts"""
        for part in parts:
            mime_type = part.get("mimeType", "")

            # Check if this part has nested parts
            if "parts" in part:
                text = extract_text_from_parts(part["parts"])
                if text:
                    return text

            # Try to get text/plain content
            if mime_type == "text/plain" and "data" in part.get("body", {}):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode()

        # If no text/plain found, try text/html as fallback
        for part in parts:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/html" and "data" in part.get("body", {}):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode()

        return None

    # Check if payload has parts (multipart message)
    if "parts" in payload:
        text = extract_text_from_parts(payload["parts"])
        if text:
            return text

    # Fallback to body data if available (simple message)
    if "body" in payload and "data" in payload["body"]:
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode()

    return ""
