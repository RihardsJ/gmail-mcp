"""Resources module for Gmail MCP Server."""

from .calendar_availability import get_calendar_availability
from .email_guidelines import get_email_guidelines

__all__ = ["get_email_guidelines", "get_calendar_availability"]
