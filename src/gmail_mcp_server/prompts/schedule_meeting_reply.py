import mcp.types as types


async def schedule_meeting_reply(arguments: dict[str, str]):
    thread_id = arguments.get("thread_id", "")
    date_range_start = arguments.get("date_range_start", "")
    date_range_end = arguments.get("date_range_end", "")
    proposed_times = arguments.get("proposed_times", "")

    prompt_message = f"""You are tasked with drafting a meeting acceptance or proposal reply with calendar context:

**CONTEXTUAL REASONING PROCESS:**

1. **Retrieve Original Email**: Use get_unread_emails to fetch thread_id: {thread_id}
   - Identify: Who is requesting the meeting?
   - Extract: What is the meeting about?
   - Check: Are specific times already proposed?

2. **Check Calendar Availability**:
   - Access calendar resource: calendar:///availability/{date_range_start}/{date_range_end}
   - Identify free slots in your calendar
   - Note: You must propose exactly 2 time slot options (per AI directive scheduling protocol)

3. **Access Guidelines**:
   - Read AI Drafting Directive (file:///ai-drafting-directive.md)
   - Review 7 Cs framework (file:///7cs-communication.md)
   - Note: Section 3.0 rule #3 - "When proposing a meeting, always offer two distinct options (date and time)"

4. **Compose Meeting Reply**:
   - If they proposed times and you're available: Accept enthusiastically
   - If you need to propose times: Offer exactly 2 specific options based on calendar availability
   - {f"Consider these proposed times: {proposed_times}" if proposed_times else "Suggest 2 alternative times from your available slots"}
   - Use UK date format: "14 December 2025"
   - Include timezone: BST or GMT as appropriate
   - Ask for agenda if not provided

5. **Apply Professional Tone**:
   - Warmly professional and enthusiastic about the meeting
   - Direct and efficient
   - Include clear CTA: "Please confirm which time works best for you"

6. **Create Draft**: Use create_draft_email tool with thread_id and reply_body

**FORMAT REQUIREMENTS:**
- Date format: DD Month YYYY (e.g., "14 December 2025")
- Time format: HH:MM AM/PM GMT/BST
- Always provide 2 time options when proposing"""

    return types.GetPromptResult(
        description=f"Draft meeting reply for thread {thread_id} with availability check",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_message),
            )
        ],
    )
