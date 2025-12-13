"""
Pytest configuration and shared fixtures.
"""

import base64
from unittest.mock import MagicMock, Mock

import pytest


@pytest.fixture
def mock_gmail_service():
    """Mock Gmail API service."""
    service = MagicMock()
    return service


@pytest.fixture
def sample_email_headers():
    """Sample email headers for testing."""
    return [
        {"name": "From", "value": "sender@example.com"},
        {"name": "Subject", "value": "Test Email"},
        {"name": "Date", "value": "Mon, 01 Jan 2024 12:00:00 +0000"},
        {"name": "Message-ID", "value": "<msg123@example.com>"},
        {"name": "References", "value": "<msg0@example.com>"},
    ]


@pytest.fixture
def sample_email_payload_simple():
    """Sample simple email payload (non-multipart)."""
    body_text = "Hello, this is a test email."
    encoded_body = base64.urlsafe_b64encode(body_text.encode()).decode()

    return {"body": {"data": encoded_body}}


@pytest.fixture
def sample_email_payload_multipart():
    """Sample multipart email payload."""
    text_plain = "Hello, this is plain text."
    text_html = "<html><body>Hello, this is HTML.</body></html>"

    return {
        "parts": [
            {
                "mimeType": "text/plain",
                "body": {
                    "data": base64.urlsafe_b64encode(text_plain.encode()).decode()
                },
            },
            {
                "mimeType": "text/html",
                "body": {"data": base64.urlsafe_b64encode(text_html.encode()).decode()},
            },
        ]
    }


@pytest.fixture
def sample_email_message(sample_email_headers, sample_email_payload_simple):
    """Sample complete email message."""
    return {
        "id": "msg123",
        "threadId": "thread456",
        "payload": {"headers": sample_email_headers, **sample_email_payload_simple},
    }


@pytest.fixture
def sample_thread():
    """Sample Gmail thread."""
    return {
        "id": "thread123",
        "messages": [
            {
                "id": "msg123",
                "threadId": "thread123",
                "payload": {
                    "headers": [
                        {"name": "From", "value": "sender@example.com"},
                        {"name": "Subject", "value": "Test Thread"},
                        {"name": "Message-ID", "value": "<msg123@example.com>"},
                        {"name": "References", "value": "<msg0@example.com>"},
                    ]
                },
            }
        ],
    }


@pytest.fixture
def mock_credentials():
    """Mock OAuth2 credentials."""
    creds = Mock()
    creds.valid = True
    creds.expired = False
    creds.refresh_token = "refresh_token"
    creds.to_json.return_value = '{"token": "test_token"}'
    return creds


@pytest.fixture
def mock_flow():
    """Mock OAuth2 flow."""
    flow = Mock()
    flow.run_local_server.return_value = Mock(
        valid=True, to_json=lambda: '{"token": "new_token"}'
    )
    return flow
