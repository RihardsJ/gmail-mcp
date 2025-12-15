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

        # Query freebusy information for all calendars
        # Reference: https://developers.google.com/workspace/calendar/api/v3/reference/freebusy/query
        logger.info("Querying freebusy information")
        freebusy_query = {
            "timeMin": start_date_time_str,
            "timeMax": end_date_time_str,
            "items": [{"id": cal_id} for cal_id in calendar_ids],
        }

        freebusy_result = (
            google_calendar_service.freebusy().query(body=freebusy_query).execute()
        )

        # Format the availability results
        calendars_info = freebusy_result.get("calendars", {})

        availability_message = "# Calendar Availability\n\n"
        availability_message += (
            f"**Time Range:** {start_date_time_str} to {end_date_time_str}\n\n"
        )

        for cal_id, cal_data in calendars_info.items():
            busy_periods = cal_data.get("busy", [])

            # Get calendar name from the list
            cal_name = next(
                (
                    cal.get("summary", cal_id)
                    for cal in calendar_list_result.get("items", [])
                    if cal.get("id") == cal_id
                ),
                cal_id,
            )

            availability_message += f"## {cal_name}\n"

            if not busy_periods:
                availability_message += "**Free** - No busy periods\n\n"
            else:
                availability_message += (
                    f"**Busy** - {len(busy_periods)} busy period(s):\n"
                )
                for period in busy_periods:
                    start = period.get("start", "N/A")
                    end = period.get("end", "N/A")
                    availability_message += f"  - {start} to {end}\n"
                availability_message += "\n"

        logger.info("Successfully retrieved calendar availability")
        return availability_message

    except HttpError as e:
        error_msg = f"Google Calendar API Error: {str(e)}"
        logger.error(error_msg)
        raise GoogleCalendarAPIError(error_msg)
    except Exception as e:
        error_msg = f"Unexpected Error retrieving calendar availability: {str(e)}"
        logger.error(error_msg)
        raise GoogleCalendarAPIError(error_msg)
