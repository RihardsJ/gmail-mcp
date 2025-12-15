"""
Snapshot tests for MCP prompts.

These tests capture the prompt content as snapshots to ensure prompts
don't change unexpectedly. When prompt engineering is intentionally
updated, regenerate snapshots with: pytest --snapshot-update
"""

import pytest

from gmail_mcp_server.server import get_prompt, list_prompts


class TestListPrompts:
    """Tests for list_prompts function."""

    @pytest.mark.asyncio
    async def test_lists_all_available_prompts(self):
        """Test that all prompts are listed."""
        prompts = await list_prompts()  # type: ignore[call-arg]

        assert len(prompts) == 3

        prompt_names = [prompt.name for prompt in prompts]
        assert "draft_professional_reply" in prompt_names
        assert "schedule_meeting_reply" in prompt_names
        assert "suggest_template" in prompt_names

    @pytest.mark.asyncio
    async def test_draft_professional_reply_prompt_schema(self):
        """Test draft_professional_reply prompt schema."""
        prompts = await list_prompts()  # type: ignore[call-arg]
        prompt = next(p for p in prompts if p.name == "draft_professional_reply")

        assert prompt.name == "draft_professional_reply"
        assert "7 Cs framework" in prompt.description
        assert "AI directive" in prompt.description
        assert len(prompt.arguments or []) == 3

        # Check arguments
        arg_names = [arg.name for arg in (prompt.arguments or [])]
        assert "thread_id" in arg_names
        assert "key_points" in arg_names
        assert "tone" in arg_names

        # Check required fields
        thread_id_arg = next(
            arg for arg in (prompt.arguments or []) if arg.name == "thread_id"
        )
        assert thread_id_arg.required is True

        key_points_arg = next(
            arg for arg in (prompt.arguments or []) if arg.name == "key_points"
        )
        assert key_points_arg.required is False

    @pytest.mark.asyncio
    async def test_schedule_meeting_reply_prompt_schema(self):
        """Test schedule_meeting_reply prompt schema."""
        prompts = await list_prompts()  # type: ignore[call-arg]
        prompt = next(p for p in prompts if p.name == "schedule_meeting_reply")

        assert prompt.name == "schedule_meeting_reply"
        assert "calendar availability" in prompt.description
        assert "2 time slots" in prompt.description
        assert len(prompt.arguments or []) == 4

        # Check arguments
        arg_names = [arg.name for arg in (prompt.arguments or [])]
        assert "thread_id" in arg_names
        assert "date_range_start" in arg_names
        assert "date_range_end" in arg_names
        assert "proposed_times" in arg_names

        # Check required fields
        required_args = [
            arg.name for arg in (prompt.arguments or []) if arg.required is True
        ]
        assert "thread_id" in required_args
        assert "date_range_start" in required_args
        assert "date_range_end" in required_args

    @pytest.mark.asyncio
    async def test_suggest_template_prompt_schema(self):
        """Test suggest_template prompt schema."""
        prompts = await list_prompts()  # type: ignore[call-arg]
        prompt = next(p for p in prompts if p.name == "suggest_template")

        assert prompt.name == "suggest_template"
        assert "template" in prompt.description
        assert "11 templates" in prompt.description
        assert len(prompt.arguments or []) == 1

        # Check arguments
        thread_id_arg = (prompt.arguments or [])[0]
        assert thread_id_arg.name == "thread_id"
        assert thread_id_arg.required is True


class TestGetPrompt:
    """Tests for get_prompt function."""

    @pytest.mark.asyncio
    async def test_raises_error_for_unknown_prompt(self):
        """Test that ValueError is raised for unknown prompt."""
        with pytest.raises(ValueError) as exc_info:
            await get_prompt("unknown_prompt", {})

        assert "Unknown prompt: unknown_prompt" in str(exc_info.value)


class TestDraftProfessionalReplyPrompt:
    """Snapshot tests for draft_professional_reply prompt."""

    @pytest.mark.asyncio
    async def test_draft_professional_reply_with_all_args(self, snapshot):
        """Test draft_professional_reply prompt content with all arguments."""
        result = await get_prompt(
            "draft_professional_reply",
            {
                "thread_id": "test_thread_123",
                "key_points": "Schedule follow-up meeting, discuss budget",
                "tone": "formal",
            },
        )

        assert (
            result.description == "Draft a formal reply to email thread test_thread_123"
        )
        assert len(result.messages) == 1
        assert result.messages[0].role == "user"

        # Snapshot the prompt content
        assert snapshot == result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_draft_professional_reply_minimal_args(self, snapshot):
        """Test draft_professional_reply prompt content with minimal arguments."""
        result = await get_prompt(
            "draft_professional_reply",
            {"thread_id": "minimal_thread_456"},
        )

        assert (
            result.description
            == "Draft a professional reply to email thread minimal_thread_456"
        )
        assert len(result.messages) == 1

        # Snapshot the prompt content
        assert snapshot == result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_draft_professional_reply_friendly_tone(self, snapshot):
        """Test draft_professional_reply with friendly tone."""
        result = await get_prompt(
            "draft_professional_reply",
            {
                "thread_id": "friendly_thread_789",
                "tone": "friendly",
            },
        )

        prompt_text = result.messages[0].content.text

        # Verify tone is mentioned
        assert "friendly" in prompt_text

        # Snapshot the prompt content
        assert snapshot == prompt_text

    @pytest.mark.asyncio
    async def test_draft_professional_reply_references_resources(self, snapshot):
        """Test that prompt references all expected resources."""
        result = await get_prompt(
            "draft_professional_reply",
            {"thread_id": "test_thread"},
        )

        prompt_text = result.messages[0].content.text

        # Verify resource references
        assert "file:///ai-drafting-directive.md" in prompt_text
        assert "file:///7cs-communication.md" in prompt_text
        assert "file:///personal-templates.md" in prompt_text

        # Verify chain of thought steps
        assert "CHAIN OF THOUGHT PROCESS" in prompt_text
        assert "Retrieve Context" in prompt_text
        assert "Analyze the Email" in prompt_text
        assert "Access Resources" in prompt_text
        assert "Apply 7 Cs Checklist" in prompt_text

        # Snapshot the prompt content
        assert snapshot == prompt_text


class TestScheduleMeetingReplyPrompt:
    """Snapshot tests for schedule_meeting_reply prompt."""

    @pytest.mark.asyncio
    async def test_schedule_meeting_reply_with_all_args(self, snapshot):
        """Test schedule_meeting_reply prompt content with all arguments."""
        result = await get_prompt(
            "schedule_meeting_reply",
            {
                "thread_id": "meeting_thread_123",
                "date_range_start": "2025-12-16",
                "date_range_end": "2025-12-20",
                "proposed_times": "Tuesday 2pm or Wednesday 3pm",
            },
        )

        assert "meeting_thread_123" in result.description
        assert len(result.messages) == 1

        # Snapshot the prompt content
        assert snapshot == result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_schedule_meeting_reply_minimal_args(self, snapshot):
        """Test schedule_meeting_reply prompt content with minimal arguments."""
        result = await get_prompt(
            "schedule_meeting_reply",
            {
                "thread_id": "meeting_456",
                "date_range_start": "2025-12-18",
                "date_range_end": "2025-12-22",
            },
        )

        prompt_text = result.messages[0].content.text

        # Verify date range is included
        assert "2025-12-18" in prompt_text
        assert "2025-12-22" in prompt_text

        # Snapshot the prompt content
        assert snapshot == prompt_text

    @pytest.mark.asyncio
    async def test_schedule_meeting_reply_references_resources(self, snapshot):
        """Test that prompt references calendar and guideline resources."""
        result = await get_prompt(
            "schedule_meeting_reply",
            {
                "thread_id": "test_meeting",
                "date_range_start": "2025-12-16",
                "date_range_end": "2025-12-20",
            },
        )

        prompt_text = result.messages[0].content.text

        # Verify resource references
        assert "calendar:///availability/2025-12-16/2025-12-20" in prompt_text
        assert "file:///ai-drafting-directive.md" in prompt_text
        assert "file:///7cs-communication.md" in prompt_text

        # Verify contextual reasoning
        assert "CONTEXTUAL REASONING PROCESS" in prompt_text
        assert "Check Calendar Availability" in prompt_text
        assert "2 time slot options" in prompt_text

        # Verify UK format requirements
        assert "DD Month YYYY" in prompt_text
        assert "GMT/BST" in prompt_text or "BST/GMT" in prompt_text

        # Snapshot the prompt content
        assert snapshot == prompt_text


class TestSuggestTemplatePrompt:
    """Snapshot tests for suggest_template prompt."""

    @pytest.mark.asyncio
    async def test_suggest_template_with_thread_id(self, snapshot):
        """Test suggest_template prompt content."""
        result = await get_prompt(
            "suggest_template",
            {"thread_id": "template_thread_123"},
        )

        assert "template_thread_123" in result.description
        assert len(result.messages) == 1

        # Snapshot the prompt content
        assert snapshot == result.messages[0].content.text

    @pytest.mark.asyncio
    async def test_suggest_template_references_templates(self, snapshot):
        """Test that prompt references template library."""
        result = await get_prompt(
            "suggest_template",
            {"thread_id": "test_thread"},
        )

        prompt_text = result.messages[0].content.text

        # Verify resource reference
        assert "file:///personal-templates.md" in prompt_text

        # Verify all 11 templates are mentioned
        assert "11 total" in prompt_text
        assert "Responding to an Appointment Reminder" in prompt_text
        assert "Responding to a Quote for Home Maintenance" in prompt_text
        assert 'Responding to a "Happy Birthday" Message' in prompt_text

        # Verify few-shot learning approach
        assert "FEW-SHOT TEMPLATE MATCHING PROCESS" in prompt_text
        assert "Pattern Matching Analysis" in prompt_text
        assert "Confidence score" in prompt_text

        # Snapshot the prompt content
        assert snapshot == prompt_text

    @pytest.mark.asyncio
    async def test_suggest_template_output_format(self, snapshot):
        """Test that prompt specifies output format."""
        result = await get_prompt(
            "suggest_template",
            {"thread_id": "format_test"},
        )

        prompt_text = result.messages[0].content.text

        # Verify output format specification
        assert "OUTPUT FORMAT" in prompt_text
        assert "RECOMMENDED TEMPLATE" in prompt_text
        assert "CONFIDENCE" in prompt_text
        assert "REASONING" in prompt_text
        assert "CUSTOMIZATION NEEDED" in prompt_text
        assert "PREVIEW" in prompt_text

        # Snapshot the prompt content
        assert snapshot == prompt_text
