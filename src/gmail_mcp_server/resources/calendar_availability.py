from ..services import get_google_calendar_api_service


async def get_calendar_availability(start_date_time_str: str, end_date_time_str: str):
    if not start_date_time_str or not end_date_time_str:
        raise ValueError(
            f"Invalid start or end date: {start_date_time_str} to {end_date_time_str}"
        )

    google_calendar_api_service = get_google_calendar_api_service()

    # Get the user's calendar IDs
    user_calendar_ids = (
        await google_calendar_api_service.calendarList().list().execute()
    )
    return f"TODO: implement availability, [{start_date_time_str}] to [{end_date_time_str}], calendar ID: {user_calendar_ids}"
