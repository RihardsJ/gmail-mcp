import mcp.types as types


async def suggest_template(arguments: dict[str, str]):
    thread_id = arguments.get("thread_id", "")

    prompt_message = f"""You are tasked with analyzing an email and suggesting the best matching template using few-shot learning:

**FEW-SHOT TEMPLATE MATCHING PROCESS:**

1. **Retrieve the Email**: Use get_unread_emails to fetch thread_id: {thread_id}

2. **Access Template Library**: Read resource file:///personal-templates.md
   - Available templates (11 total):
     1. Responding to an Appointment Reminder
     2. Responding to a Quote for Home Maintenance
     3. Responding to a "Happy Birthday" Message
     4. Responding to a Neighbor's Email
     5. Responding to a School or Teacher's Email
     6. Responding to an Inquiry about an Item You're Selling Online
     7. Responding to a Bill or Invoice Question
     8. Responding to a Follow-Up from a Service Provider
     9. Responding to a "Checking In" Email from a Friend
     10. Responding to a Request for a Personal Reference
     11. Responding to an Online Order Confirmation

3. **Pattern Matching Analysis**:
   - Identify email type/category
   - Match sender type (friend/business/service provider/etc.)
   - Match intent (confirmation/question/social/transaction)
   - Match context indicators (keywords like "appointment", "quote", "birthday", "meeting", etc.)

4. **Reasoning Process** (Few-Shot Learning):
   - Compare email characteristics with each template's use case
   - Score relevance of each template (0-10)
   - Identify top 2-3 potential matches
   - Select best match with confidence score

5. **Present Recommendation**:
   - Template name and number
   - Confidence score (0-100%)
   - Reasoning for selection
   - Key fields to customize [Name, Date, Amount, etc.]
   - Optional: Show populated template preview

6. **Alternative Suggestions**:
   - If no template matches well (confidence < 60%): Recommend custom draft
   - If multiple templates match: Suggest the top 2 with trade-offs

**OUTPUT FORMAT:**
```
**RECOMMENDED TEMPLATE:** [Template Name]
**CONFIDENCE:** [X]%
**REASONING:** [Why this template matches]
**CUSTOMIZATION NEEDED:** [List of fields to fill in]
**PREVIEW:** [Show template with placeholders filled]
```"""

    return types.GetPromptResult(
        description=f"Suggest best template match for email thread {thread_id}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=prompt_message),
            )
        ],
    )
