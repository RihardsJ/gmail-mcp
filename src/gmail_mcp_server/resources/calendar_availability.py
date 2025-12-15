async def get_calendar_availability(start_date_time_str: str, end_date_time_str: str):
    if not start_date_time_str or not end_date_time_str:
        raise ValueError(
            f"Invalid start or end date: {start_date_time_str} to {end_date_time_str}"
        )

    return f"TODO: implement availability, [{start_date_time_str}] to [{end_date_time_str}]"
