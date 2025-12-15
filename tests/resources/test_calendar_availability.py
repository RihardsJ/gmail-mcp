"""
Tests for calendar availability resources module.
"""

from unittest.mock import Mock, patch

import pytest

from gmail_mcp_server.resources.calendar_availability import (
    GoogleCalendarAPIError,
    get_calendar_availability,
)


class TestGetCalendarAvailability:
    """Tests for get_calendar_availability function."""

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_retrieves_availability_successfully(self, mock_get_service):
        """Test successful retrieval of calendar availability."""
        # Setup mock service
        mock_service = Mock()

        # Mock calendar list
        mock_calendar_list = Mock()
        mock_calendar_list.execute.return_value = {
            "items": [
                {"id": "primary", "summary": "My Calendar"},
                {"id": "[email protected]", "summary": "Work Calendar"},
            ]
        }
        mock_service.calendarList().list.return_value = mock_calendar_list

        # Mock freebusy query
        mock_freebusy_query = Mock()
        mock_freebusy_query.execute.return_value = {
            "calendars": {
                "primary": {
                    "busy": [
                        {
                            "start": "2025-01-15T10:00:00Z",
                            "end": "2025-01-15T11:00:00Z",
                        }
                    ]
                },
                "[email protected]": {"busy": []},
            }
        }
        mock_service.freebusy().query.return_value = mock_freebusy_query

        mock_get_service.return_value = mock_service

        # Execute
        result = await get_calendar_availability(
            "2025-01-15T09:00:00Z", "2025-01-15T17:00:00Z"
        )

        # Verify
        assert "# Calendar Availability" in result
        assert "My Calendar" in result
        assert "Work Calendar" in result
        assert "**Busy**" in result
        assert "**Free**" in result
        assert "2025-01-15T10:00:00Z to 2025-01-15T11:00:00Z" in result

        # Verify API calls
        mock_service.calendarList().list.assert_called_once()
        mock_service.freebusy().query.assert_called_once()

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_freebusy_query_with_correct_parameters(self, mock_get_service):
        """Test that freebusy query is called with correct parameters."""
        mock_service = Mock()

        mock_calendar_list = Mock()
        mock_calendar_list.execute.return_value = {
            "items": [{"id": "primary", "summary": "Calendar"}]
        }
        mock_service.calendarList().list.return_value = mock_calendar_list

        mock_freebusy_query = Mock()
        mock_freebusy_query.execute.return_value = {
            "calendars": {"primary": {"busy": []}}
        }
        mock_service.freebusy().query.return_value = mock_freebusy_query

        mock_get_service.return_value = mock_service

        start_time = "2025-01-15T09:00:00Z"
        end_time = "2025-01-15T17:00:00Z"

        await get_calendar_availability(start_time, end_time)

        # Verify freebusy query was called with correct body
        call_args = mock_service.freebusy().query.call_args
        body = call_args[1]["body"]

        assert body["timeMin"] == start_time
        assert body["timeMax"] == end_time
        assert body["items"] == [{"id": "primary"}]

    @pytest.mark.asyncio
    async def test_raises_error_for_empty_start_date(self):
        """Test that empty start date raises GoogleCalendarAPIError."""
        with pytest.raises(GoogleCalendarAPIError, match="Invalid start or end date"):
            await get_calendar_availability("", "2025-01-15T17:00:00Z")

    @pytest.mark.asyncio
    async def test_raises_error_for_empty_end_date(self):
        """Test that empty end date raises GoogleCalendarAPIError."""
        with pytest.raises(GoogleCalendarAPIError, match="Invalid start or end date"):
            await get_calendar_availability("2025-01-15T09:00:00Z", "")

    @pytest.mark.asyncio
    async def test_raises_error_for_none_dates(self):
        """Test that None dates raise GoogleCalendarAPIError."""
        with pytest.raises(GoogleCalendarAPIError, match="Invalid start or end date"):
            await get_calendar_availability(None, None)  # type: ignore

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_handles_http_error(self, mock_get_service):
        """Test handling of HTTP errors from Google Calendar API."""
        from googleapiclient.errors import HttpError

        mock_service = Mock()
        mock_service.calendarList().list().execute.side_effect = HttpError(
            resp=Mock(status=403), content=b"Access denied"
        )
        mock_get_service.return_value = mock_service

        with pytest.raises(GoogleCalendarAPIError, match="Google Calendar API Error"):
            await get_calendar_availability(
                "2025-01-15T09:00:00Z", "2025-01-15T17:00:00Z"
            )

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_handles_all_calendars_free(self, mock_get_service):
        """Test output when all calendars are free."""
        mock_service = Mock()

        mock_calendar_list = Mock()
        mock_calendar_list.execute.return_value = {
            "items": [
                {"id": "cal1", "summary": "Calendar 1"},
                {"id": "cal2", "summary": "Calendar 2"},
            ]
        }
        mock_service.calendarList().list.return_value = mock_calendar_list

        mock_freebusy_query = Mock()
        mock_freebusy_query.execute.return_value = {
            "calendars": {
                "cal1": {"busy": []},
                "cal2": {"busy": []},
            }
        }
        mock_service.freebusy().query.return_value = mock_freebusy_query

        mock_get_service.return_value = mock_service

        result = await get_calendar_availability(
            "2025-01-15T09:00:00Z", "2025-01-15T17:00:00Z"
        )

        assert "Calendar 1" in result
        assert "Calendar 2" in result
        assert result.count("**Free**") == 2
        assert "**Busy**" not in result

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_handles_multiple_busy_periods(self, mock_get_service):
        """Test output with multiple busy periods."""
        mock_service = Mock()

        mock_calendar_list = Mock()
        mock_calendar_list.execute.return_value = {
            "items": [{"id": "primary", "summary": "My Calendar"}]
        }
        mock_service.calendarList().list.return_value = mock_calendar_list

        mock_freebusy_query = Mock()
        mock_freebusy_query.execute.return_value = {
            "calendars": {
                "primary": {
                    "busy": [
                        {
                            "start": "2025-01-15T10:00:00Z",
                            "end": "2025-01-15T11:00:00Z",
                        },
                        {
                            "start": "2025-01-15T14:00:00Z",
                            "end": "2025-01-15T15:00:00Z",
                        },
                        {
                            "start": "2025-01-15T16:00:00Z",
                            "end": "2025-01-15T17:00:00Z",
                        },
                    ]
                }
            }
        }
        mock_service.freebusy().query.return_value = mock_freebusy_query

        mock_get_service.return_value = mock_service

        result = await get_calendar_availability(
            "2025-01-15T09:00:00Z", "2025-01-15T18:00:00Z"
        )

        assert "**Busy** - 3 busy period(s)" in result
        assert "2025-01-15T10:00:00Z to 2025-01-15T11:00:00Z" in result
        assert "2025-01-15T14:00:00Z to 2025-01-15T15:00:00Z" in result
        assert "2025-01-15T16:00:00Z to 2025-01-15T17:00:00Z" in result

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_handles_calendar_without_summary(self, mock_get_service):
        """Test handling of calendars without summary field."""
        mock_service = Mock()

        mock_calendar_list = Mock()
        mock_calendar_list.execute.return_value = {
            "items": [{"id": "[email protected]"}]  # No summary
        }
        mock_service.calendarList().list.return_value = mock_calendar_list

        mock_freebusy_query = Mock()
        mock_freebusy_query.execute.return_value = {
            "calendars": {"[email protected]": {"busy": []}}
        }
        mock_service.freebusy().query.return_value = mock_freebusy_query

        mock_get_service.return_value = mock_service

        result = await get_calendar_availability(
            "2025-01-15T09:00:00Z", "2025-01-15T17:00:00Z"
        )

        # Should use calendar ID as fallback
        assert "[email protected]" in result

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_includes_time_range_in_output(self, mock_get_service):
        """Test that time range is included in output."""
        mock_service = Mock()

        mock_calendar_list = Mock()
        mock_calendar_list.execute.return_value = {"items": []}
        mock_service.calendarList().list.return_value = mock_calendar_list

        mock_freebusy_query = Mock()
        mock_freebusy_query.execute.return_value = {"calendars": {}}
        mock_service.freebusy().query.return_value = mock_freebusy_query

        mock_get_service.return_value = mock_service

        start = "2025-01-15T09:00:00Z"
        end = "2025-01-15T17:00:00Z"

        result = await get_calendar_availability(start, end)

        assert "# Calendar Availability" in result
        assert f"**Time Range:** {start} to {end}" in result

    @pytest.mark.asyncio
    @patch(
        "gmail_mcp_server.resources.calendar_availability.get_google_calendar_api_service"
    )
    async def test_handles_unexpected_exception(self, mock_get_service):
        """Test handling of unexpected exceptions."""
        mock_service = Mock()
        mock_service.calendarList().list().execute.side_effect = Exception(
            "Unexpected error"
        )
        mock_get_service.return_value = mock_service

        with pytest.raises(
            GoogleCalendarAPIError,
            match="Unexpected Error retrieving calendar availability",
        ):
            await get_calendar_availability(
                "2025-01-15T09:00:00Z", "2025-01-15T17:00:00Z"
            )
