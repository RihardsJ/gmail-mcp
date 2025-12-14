"""
Tests for MCP server module.
"""

from unittest.mock import MagicMock, patch

import pytest

from gmail_mcp_server.server import handle_call_tool, handle_list_tools


class TestHandleListTools:
    """Tests for handle_list_tools function."""

    @pytest.mark.asyncio
    async def test_lists_all_available_tools(self):
        """Test that all tools are listed."""
        tools = await handle_list_tools()  # type: ignore[call-arg]

        assert len(tools) == 2

        tool_names = [tool.name for tool in tools]
        assert "get_unread_emails" in tool_names
        assert "create_draft_email" in tool_names

    @pytest.mark.asyncio
    async def test_get_unread_emails_tool_schema(self):
        """Test get_unread_emails tool schema."""
        tools = await handle_list_tools()  # type: ignore[call-arg]
        get_unread_tool = next(t for t in tools if t.name == "get_unread_emails")

        assert get_unread_tool.description == "Get unread emails"
        assert get_unread_tool.inputSchema["type"] == "object"
        assert "limit" in get_unread_tool.inputSchema["properties"]
        assert get_unread_tool.inputSchema["properties"]["limit"]["type"] == "integer"

    @pytest.mark.asyncio
    async def test_create_draft_email_tool_schema(self):
        """Test create_draft_email tool schema."""
        tools = await handle_list_tools()  # type: ignore[call-arg]
        create_draft_tool = next(t for t in tools if t.name == "create_draft_email")

        assert create_draft_tool.description == "Create a draft email"
        assert create_draft_tool.inputSchema["type"] == "object"
        assert "thread_id" in create_draft_tool.inputSchema["properties"]
        assert "reply_body" in create_draft_tool.inputSchema["properties"]
        assert "thread_id" in create_draft_tool.inputSchema["required"]
        assert "reply_body" in create_draft_tool.inputSchema["required"]

    @pytest.mark.asyncio
    async def test_tool_schemas_have_descriptions(self):
        """Test that all tool parameters have descriptions."""
        tools = await handle_list_tools()  # type: ignore[call-arg]

        for tool in tools:
            properties = tool.inputSchema.get("properties", {})
            for param_name, param_schema in properties.items():
                assert "description" in param_schema, (
                    f"Parameter {param_name} in tool {tool.name} missing description"
                )


class TestHandleCallTool:
    """Tests for handle_call_tool function."""

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.get_unread_emails")
    async def test_calls_get_unread_emails_tool(self, mock_get_unread):
        """Test calling get_unread_emails tool."""
        mock_get_unread.return_value = []

        await handle_call_tool("get_unread_emails", {"limit": 10})

        mock_get_unread.assert_called_once_with(10)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.get_unread_emails")
    async def test_get_unread_emails_uses_default_limit(self, mock_get_unread):
        """Test get_unread_emails uses default limit from config."""
        mock_get_unread.return_value = []

        await handle_call_tool("get_unread_emails", {})

        # Default limit should be used from config (max_email_limit = 5)
        mock_get_unread.assert_called_once_with(5)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.create_draft_reply")
    async def test_calls_create_draft_email_tool(self, mock_create_draft):
        """Test calling create_draft_email tool."""
        mock_create_draft.return_value = []
        arguments = {"thread_id": "thread123", "reply_body": "Test reply"}

        await handle_call_tool("create_draft_email", arguments)

        mock_create_draft.assert_called_once_with(arguments)

    @pytest.mark.asyncio
    async def test_raises_error_for_unknown_tool(self):
        """Test that ValueError is raised for unknown tool."""
        with pytest.raises(ValueError) as exc_info:
            await handle_call_tool("unknown_tool", {})

        assert "Unknown tool: unknown_tool" in str(exc_info.value)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.get_unread_emails")
    async def test_get_unread_emails_returns_results(self, mock_get_unread):
        """Test that get_unread_emails results are returned."""
        mock_results = [MagicMock(type="text", text="Email 1")]
        mock_get_unread.return_value = mock_results

        results = await handle_call_tool("get_unread_emails", {"limit": 1})

        assert results == mock_results

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.create_draft_reply")
    async def test_create_draft_email_returns_results(self, mock_create_draft):
        """Test that create_draft_email results are returned."""
        mock_results = [MagicMock(type="text", text="Draft created")]
        mock_create_draft.return_value = mock_results

        arguments = {"thread_id": "thread123", "reply_body": "Reply"}
        results = await handle_call_tool("create_draft_email", arguments)

        assert results == mock_results

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.get_unread_emails")
    async def test_passes_limit_argument_correctly(self, mock_get_unread):
        """Test that limit argument is passed correctly."""
        mock_get_unread.return_value = []

        await handle_call_tool("get_unread_emails", {"limit": 20})

        mock_get_unread.assert_called_once_with(20)

    @pytest.mark.asyncio
    @patch("gmail_mcp_server.server.create_draft_reply")
    async def test_passes_draft_arguments_correctly(self, mock_create_draft):
        """Test that draft arguments are passed correctly."""
        mock_create_draft.return_value = []
        arguments = {
            "thread_id": "thread_xyz",
            "reply_body": "Custom reply body",
        }

        await handle_call_tool("create_draft_email", arguments)

        mock_create_draft.assert_called_once_with(arguments)
