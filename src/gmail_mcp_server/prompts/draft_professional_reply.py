import mcp.types as types


async def draft_professional_reply(arguments: dict[str, str]):
    thread_id = arguments.get("thread_id", "")
    key_points = arguments.get("key_points", "")
    tone = arguments.get("tone", "professional")

    prompt_message = f"""You are tasked with drafting a professional email reply following these strict guidelines:

**CHAIN OF THOUGHT PROCESS:**

1. **Retrieve Context**: First, use the get_unread_emails tool to retrieve the original email for thread_id: {thread_id}

2. **Analyze the Email**:
- Identify the sender's tone and relationship level
- Extract key requests, questions, or action items
- Determine appropriate response category (personal/internal/external/formal)

3. **Access Resources**:
- Read the AI Drafting Directive resource (file:///ai-drafting-directive.md) to understand your voice and persona
- Read the 7 Cs framework resource (file:///7cs-communication.md) for quality standards
- Consider if any personal templates (file:///personal-templates.md) are relevant

4. **Draft the Reply**:
- Use first-person voice (I/we)
- Tone: {tone}
- Include these key points: {key_points if key_points else "Address all points from the original email"}
- Apply your persona from the AI directive
- Ensure one clear Call-to-Action (CTA)

5. **Apply 7 Cs Checklist**:
- Clear: Purpose is immediately understood
- Concise: No unnecessary words
- Concrete: Specific facts, dates, times
- Correct: UK English spelling and grammar
- Coherent: Logical flow
- Complete: All necessary information included
- Courteous: Professional and respectful

6. **Final Review**:
- Verify signature: "Rihards J\\nrihards.jukna@gmail.com"
- Check UK date/time formats if applicable
- Ensure tone matches the desired level: {tone}

7. **Create Draft**: Use the create_draft_email tool with thread_id and your composed reply_body

**IMPORTANT**: Think through each step before acting. Explain your reasoning for tone and structure choices."""

    return types.GetPromptResult(
        description=f"Draft a {tone} reply to email thread {thread_id}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_message),
            )
        ],
    )
