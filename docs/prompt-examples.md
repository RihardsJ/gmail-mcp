# Example Prompts for Gmail MCP Server

This document provides example prompts to demonstrate the capabilities of the Gmail MCP Server with Claude Desktop.

## Table of Contents

1. [Basic Email Operations](#basic-email-operations)
2. [Advanced MCP Prompts](#advanced-mcp-prompts)
3. [Resource-Enhanced Drafting](#resource-enhanced-drafting)
4. [Calendar-Integrated Replies](#calendar-integrated-replies)

---

## Basic Email Operations

These prompts use the core MCP tools directly.

### Read Unread Emails

```
Show me my 3 most recent unread emails and provide a brief summary of each one, including who sent it and what it's about.
```

**What happens:** Claude uses the `get_unread_emails` tool to fetch your unread messages and summarizes them.

---

### Create a Simple Draft Reply

```
Check my unread emails. For the first one, draft a professional reply thanking the sender and saying I'll get back to them by end of week. Keep it friendly and concise.
```

**What happens:** Claude reads your emails, then uses `create_draft_reply` to create a threaded draft in your Gmail account.

---

### Email Triage

```
Look at my 5 most recent unread emails. Categorize them by urgency (high/medium/low) based on the content and sender. Then, draft a polite reply to the most urgent one, acknowledging the request and providing a timeline for response.
```

**What happens:** Claude analyzes multiple emails and prioritizes them before drafting a response.

---

## Advanced MCP Prompts

These prompts leverage the sophisticated MCP prompts built into the server.

### 1. Professional Reply with 7 Cs Framework

```
Use the draft_professional_reply prompt with my first unread email. I need to confirm receipt of the quarterly report and mention that I'll review it by Friday. Use a professional tone.
```

**What happens:** 
- Uses the `draft_professional_reply` MCP prompt
- Applies chain-of-thought reasoning through 7 steps
- Validates against the 7 Cs of Communication (Clarity, Conciseness, Correctness, etc.)
- Incorporates your AI directive persona
- Outputs UK English formatting

**MCP Prompt Arguments:**
- `thread_id`: Automatically selected from first unread
- `key_points`: "confirm receipt, review by Friday"
- `tone`: "professional"

---

### 2. Meeting Scheduling with Calendar Context

```
Use the schedule_meeting_reply prompt for the email from John about next week's planning session. Check my availability from December 16-20, 2025.
```

**What happens:**
- Uses the `schedule_meeting_reply` MCP prompt
- Integrates real-time calendar availability via Google Calendar API
- Proposes 2 specific time slots following your AI directive protocol
- UK date/time format with timezone (BST/GMT)
- Applies 7 Cs framework for professionalism

**MCP Prompt Arguments:**
- `thread_id`: From John's email
- `date_range_start`: "2025-12-16"
- `date_range_end`: "2025-12-20"

---

### 3. Template Suggestion with Reasoning

```
Use the suggest_template prompt to analyze my unread email from the dentist office.
```

**What happens:**
- Uses the `suggest_template` MCP prompt with few-shot learning
- Analyzes email content against 11 personal templates
- Returns template match with confidence score (0-100%)
- Explains reasoning for selection
- Shows which template fields need customization
- Provides pre-populated template preview

**Example Output:**
```
Template Match: "Appointment Confirmation" (95% confidence)
Reasoning: Email contains appointment details and time confirmation
Required Fields: [date], [time], [location]
Preview: 
"Dear [Practice Name],

Thank you for confirming my appointment on [date] at [time].
I look forward to seeing you then.

Best regards"
```

---

## Resource-Enhanced Drafting

These prompts demonstrate how Claude uses the MCP resources for higher-quality email composition.

### Using the 7 Cs Framework

```
Draft a reply to Sarah's budget request email. Make sure to follow the 7 Cs of Effective Communication framework. I need to explain that we need to reduce the proposed budget by 15% and suggest a follow-up meeting to discuss alternatives.
```

**What happens:**
- Claude accesses `file:///email-guidelines/7cs-communication.md` resource
- Ensures the draft meets all 7 criteria:
  - **Clarity**: Clear message about budget reduction
  - **Conciseness**: No unnecessary words
  - **Correctness**: Accurate 15% figure
  - **Coherence**: Logical flow of ideas
  - **Completeness**: Includes next steps (meeting)
  - **Courtesy**: Respectful tone despite delivering bad news
  - **Concreteness**: Specific numbers and actions

---

### Using Personal Email Templates

```
I received an email asking for a quote on garden maintenance. Draft a reply using one of my personal email templates.
```

**What happens:**
- Claude accesses `file:///email-guidelines/personal-templates.md` resource
- Identifies the "Request for Quote" template
- Customizes it with context from the received email
- Maintains your personal communication style

**Template Used:**
```
Subject: Re: Quote Request for Garden Maintenance

Dear [Name],

Thank you for reaching out regarding [service]. I'd be happy to provide a quote.

To give you an accurate estimate, I'll need a few more details:
- [Detail 1]
- [Detail 2]
- [Detail 3]

Once I have this information, I'll send over a detailed quote within [timeframe].

Best regards
```

---

### Using AI Drafting Directive

```
Draft a reply to the complaint email from our client about the delayed delivery. Use my AI drafting directive to ensure we apply proper empathy and problem-solving approach.
```

**What happens:**
- Claude accesses `file:///email-guidelines/ai-drafting-directive.md` resource
- Applies Dale Carnegie principles (empathy, acknowledge feelings)
- Uses Robert Cialdini's reciprocity and consistency principles
- Follows Stephen Covey's seek-first-to-understand approach
- Maps to appropriate tone (apologetic + solution-focused)
- UK English spelling and formatting

**Directive Principles Applied:**
- Acknowledges client's frustration first
- Takes responsibility without making excuses
- Offers specific remedy/compensation
- Commits to preventing future issues
- Ends on a relationship-building note

---

### Combining All Resources

```
Check my unread emails. For the one from Mark about the project timeline, draft a professional reply using the 7 Cs framework, my AI directive, and check if any of my templates apply. I need to apologize for the 2-week delay and propose a revised timeline with a meeting to discuss.
```

**What happens:**
- Accesses all three resources:
  1. 7 Cs framework for structure
  2. AI directive for tone and persuasion tactics
  3. Personal templates for format (if applicable)
- Creates a comprehensive, professional response
- Balances apology with solution-oriented approach

---

## Calendar-Integrated Replies

These prompts showcase the Google Calendar integration for context-aware scheduling.

### Accept Meeting with Availability Context

```
Check my unread meeting requests. For the one from Jane, accept it and propose 2 alternative times based on my calendar availability this week.
```

**What happens:**
- Uses `get_calendar_availability` tool
- Analyzes your actual free/busy status
- Proposes specific time slots when you're available
- Follows your AI directive's "always offer 2 options" protocol

---

### Decline with Alternative Times

```
Draft a reply declining the Monday 9am meeting from HR, but offer 2 alternative times between December 18-20 when I'm actually free.
```

**What happens:**
- Politely declines with reasoning
- Queries calendar for genuine availability
- Suggests concrete alternatives
- Maintains professional tone per AI directive

---

## Tips for Best Results

1. **Be Specific**: Include key points you want to address in your reply
2. **Mention Resources**: Explicitly ask Claude to use the 7 Cs, templates, or AI directive when you want that level of quality
3. **Use MCP Prompts**: Call the advanced prompts by name for sophisticated multi-step reasoning
4. **Provide Context**: The more context you give about the situation, the better the draft
5. **Iterate**: Review drafts and ask Claude to refine them before sending

---

## What Gets Created

All drafts are created in your **Gmail Drafts folder**. They are:
-  Correctly threaded to the original email
-  Ready for your review and editing
-  Not sent automatically (you stay in control)
