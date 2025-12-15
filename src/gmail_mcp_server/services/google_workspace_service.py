"""
Build the Gmail API service.

Returns:
    Gmail API service object.

Reference: https://developers.google.com/workspace/gmail/api/quickstart/python
"""

from logging import getLogger

from googleapiclient.discovery import build

from ..configs import configs
from .google_oauth_credentials import get_google_oauth_credentials

SCOPES = configs.get("google_scopes")
CLIENT_SECRETS_FILE = configs.get("client_secrets_file")
TOKEN_FILE = configs.get("token_file")


logger = getLogger(__name__)
logger.info("Scopes: %s", SCOPES)


def get_gmail_api_service():
    logger.info("Building gmail api service...")
    return build("gmail", "v1", credentials=get_google_oauth_credentials())


def get_google_drive_api_service():
    logger.info("Building google drive api service...")
    return build("drive", "v3", credentials=get_google_oauth_credentials())


def get_google_calendar_api_service():
    logger.info("Building google calendar api service...")
    return build("calendar", "v3", credentials=get_google_oauth_credentials())
