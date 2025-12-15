#!/usr/bin/env python3

"""Email guidelines resources for AI-assisted email drafting."""

import logging
from typing import Literal

from googleapiclient.errors import HttpError

from ..configs import configs
from ..services import get_google_drive_api_service

logger = logging.getLogger(__name__)

# Define allowed guideline names based on settings.toml [default.google_docs]
GuidelineName = Literal["7cs", "email_templates", "directive"]


class GoogleDriveAPIError(Exception):
    """Exception raised when there is an error with the Google Drive API."""

    pass


async def get_email_guidelines(
    guideline_name: GuidelineName,
) -> bytes:
    """
    Retrieves email guideline documents from Google Drive.

    The guideline documents are stored as Google Docs and exported as markdown.

    Reference:  https://developers.google.com/drive/api/v3/reference/files/export
                https://developers.google.com/drive/api/guides/ref-export-formats
    parameters:
        guideline_name (GuidelineName): The name of the guideline to retrieve.
                                       Must be one of: '7cs', 'email_templates', 'directive'

    returns:
        bytes: The guideline document content in markdown format as bytes.

    raises:
        GoogleDriveAPIError: If there's an error retrieving the guideline or invalid guideline name.

    example:
        await get_email_guidelines('7cs')
    """

    # Define valid guideline names
    VALID_GUIDELINES = {"7cs", "email_templates", "directive"}

    try:
        logger.debug(f"Retrieving guideline: {guideline_name}")

        # Validate guideline name
        if guideline_name not in VALID_GUIDELINES:
            error_msg = (
                f"Invalid guideline name: '{guideline_name}'. "
                f"Must be one of: {', '.join(sorted(VALID_GUIDELINES))}"
            )
            logger.error(error_msg)
            raise GoogleDriveAPIError(error_msg)

        # Get the document ID from config
        doc_file_id = configs.get(f"google_docs.{guideline_name}_doc_id")

        if not doc_file_id:
            error_msg = f"No document ID found for guideline: {guideline_name}"
            logger.error(error_msg)
            raise GoogleDriveAPIError(error_msg)

        logger.info(f"Exporting Google Doc {doc_file_id} as markdown")
        google_drive_service = get_google_drive_api_service()

        # Export the Google Doc as markdown (returns bytes)
        guideline_doc = (
            google_drive_service.files()
            .export(fileId=doc_file_id, mimeType="text/markdown")
            .execute()
        )

        logger.info(f"Successfully retrieved guideline: {guideline_name}")

        return guideline_doc

    except HttpError as e:
        error_msg = f"Google Drive API Error: {str(e)}"
        logger.error(error_msg)
        raise GoogleDriveAPIError(error_msg)
    except Exception as e:
        logger.error(
            f"Unexpected Error retrieving guideline '{guideline_name}': {str(e)}"
        )
        raise GoogleDriveAPIError(
            f"Unexpected Error retrieving guideline '{guideline_name}': {str(e)}"
        )
