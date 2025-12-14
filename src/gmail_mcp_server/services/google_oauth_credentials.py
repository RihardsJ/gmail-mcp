import os.path
from logging import getLogger

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from ..configs import configs

SCOPES = configs.get("google_scopes")
CLIENT_SECRETS_FILE = configs.get("client_secrets_file")
TOKEN_FILE = configs.get("token_file")


logger = getLogger(__name__)


def get_google_oauth_credentials():
    """
    Get or refresh Google OAuth credentials.
    Reference: https://developers.google.com/workspace/gmail/api/quickstart/python
    """
    logger.info("Getting google oauth credentials...")
    creds = None
    # First check if there are valid credentials available
    if os.path.exists(TOKEN_FILE):
        logger.info("Loading existing credentials from file.")
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing existing credentials.")
            creds.refresh(Request())
        else:
            logger.info("Requesting new credentials google. Initializing OAuth flow.")
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES
            )
            creds = flow.run_local_server(
                port=8100,
                success_message="Successfully authorized! You can now close this window.",
            )
        # Save the credentials for the next run
        logger.info("Saving credentials to file.")
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())
    return creds
