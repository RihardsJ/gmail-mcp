#!/usr/bin/env python3

"""Calendar availability resources for checking user's calendar."""

import logging

from googleapiclient.errors import HttpError

from ..services import get_google_calendar_api_service

logger = logging.getLogger(__name__)


class GoogleCalendarAPIError(Exception):
    """Exception raised when there is an error with the Google Calendar API."""

    pass


async def get_calendar_availability(
    start_date_time_str: str, end_date_time_str: str
) -> str:
    """
    Retrieves calendar availability for a given time range.

    Reference: https://developers.google.com/calendar/api/v3/reference

    parameters:
        start_date_time_str (str): Start date/time in ISO 8601 format
        end_date_time_str (str): End date/time in ISO 8601 format

    returns:
        str: Calendar availability information

    raises:
        GoogleCalendarAPIError: If there's an error retrieving calendar data
        ValueError: If date parameters are invalid

    example:
        await get_calendar_availability('2025-01-01T09:00:00Z', '2025-01-01T17:00:00Z')
    """

    try:
        logger.debug(
            f"Retrieving calendar availability from {start_date_time_str} to {end_date_time_str}"
        )

        # Validate inputs
        if not start_date_time_str or not end_date_time_str:
            error_msg = f"Invalid start or end date: {start_date_time_str} to {end_date_time_str}"
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info("Fetching Google Calendar service")
        google_calendar_service = get_google_calendar_api_service()

        # Get the user's calendar IDs (synchronous call, no await)
        logger.info("Retrieving user's calendar list")
        calendar_list_result = google_calendar_service.calendarList().list().execute()

        calendar_ids = [cal["id"] for cal in calendar_list_result.get("items", [])]

        logger.info(f"Found {len(calendar_ids)} calendars")

        # TODO: Implement actual availability check using freebusy query
        # For now, return calendar IDs
        result = (
            f"TODO: implement availability check\n"
            f"Time range: {start_date_time_str} to {end_date_time_str}\n"
            f"Calendar IDs: {', '.join(calendar_ids)}"
        )

        logger.info("Successfully retrieved calendar information")
        return result

    except HttpError as e:
        error_msg = f"Google Calendar API Error: {str(e)}"
        logger.error(error_msg)
        raise GoogleCalendarAPIError(error_msg)
    except ValueError as e:
        # Re-raise ValueError as-is
        raise
    except Exception as e:
        error_msg = f"Unexpected Error retrieving calendar availability: {str(e)}"
        logger.error(error_msg)
        raise GoogleCalendarAPIError(error_msg)
