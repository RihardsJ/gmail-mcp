# 📬️ Gmail MCP Server

## Overview

This project is a Model Context Protocol (MCP) server that enables AI assistants like Claude to interact with Gmail accounts. This server provides tools for reading unread emails and creating draft replies, allowing seamless email management through natural language conversations.

- **Built for**: MCP Foundation Project Assessment
- **Tech Stack**: Python 3.11+, Python MCP SDK, Gmail API, OAuth2
- **Target**: Claude Desktop Integration (compatible with any MCP client)

## Core Features

- **Email Retrieval**: Fetch unread emails from Gmail.
- **Draft Creation**: Create draft replies for selected emails.
- **Message Management**: Mark emails as read or unread, delete emails.
- **AI-Assisted Email Drafting**: Professional writing guidelines and templates via MCP resources and prompts.
- **Google Docs Integration**: Optionally fetch email guidelines from Google Docs for centralized management.

## MCP Capabilities

### Tools

- **`get_unread_emails`**: Returns sender, subject, body/snippet, and email/thread ID
- **`create_draft_reply`**: Creates correctly threaded draft replies from original email/thread ID and reply body

### Resources

- **`file:///email-guidelines/7cs-communication.md`**: The 7 Cs of Effective Communication framework
- **`file:///email-guidelines/personal-templates.md`**: 11 personal email templates for common tasks
- **`file:///email-guidelines/ai-drafting-directive.md`**: Comprehensive AI email drafting directive with persona and persuasion tactics

## Stretch Goals 

### 1. Professional Writing Framework via MCP Resources

Exposed three comprehensive resources that Claude can access when drafting emails:

- **7 Cs of Communication** (`file:///email-guidelines/7cs-communication.md`)
  - Professional framework ensuring emails are: Clear, Concise, Correct, Coherent, Complete, Courteous, and Concrete
  - Automatically applied when using the `draft_professional_reply` prompt

- **Personal Email Templates** (`file:///email-guidelines/personal-templates.md`)
  - 11 ready-to-use templates for common scenarios (appointments, quotes, neighbor communications, etc.)
  - Accessible via the `suggest_template` prompt with AI-powered matching

- **AI Drafting Directive** (`file:///email-guidelines/ai-drafting-directive.md`)
  - Incorporates principles from Dale Carnegie, Robert Cialdini, and Stephen Covey
  - Defines persona, tone mapping, and ethical persuasion tactics
  - Ensures consistent voice across all communications

### 2. Advanced MCP Prompts with Prompt Engineering

Implemented three sophisticated prompts demonstrating different prompt engineering techniques:

| Prompt | Technique | Purpose |
|--------|-----------|---------|
| `draft_professional_reply` | Chain of Thought | 7-step reasoning process for professional emails |
| `schedule_meeting_reply` | Contextual Prompting | Calendar-integrated meeting scheduling |
| `suggest_template` | Few-Shot Learning | AI-powered template matching with confidence scoring |

### 3. Google Docs Integration (Optional)

- Fetch email guidelines directly from Google Docs for centralized, team-shareable documentation
- Automatic fallback to local markdown files if Google Docs unavailable
- Supports collaborative guideline updates without code changes
- Configurable via `settings.toml` with document IDs

### 4. Google Calendar Integration (Optional)

- Real-time availability checking via Google Calendar API
- The `schedule_meeting_reply` prompt automatically proposes times when you're actually free
- Follows the "always offer 2 time slot options" protocol from the AI directive

**Impact**: These enhancements transform basic email drafting into a sophisticated, context-aware system that maintains professional standards and personal voice while saving time.

---

## Project Milestones

### Core Requirements

- [x] **Gmail API Setup**: Google Cloud project, OAuth2 configuration, scopes
- [x] **MCP Server**: Python implementation with mcp SDK
- [x] **Authorization**: OAuth2 authentication for Gmail API
- [x] **Email Retrieval Tool**: `get_unread_emails` with required fields
- [x] **Draft Reply Tool**: `create_draft_reply` with threading
- [x] **Claude Desktop Integration**: Local server configuration and testing
- [x] **Documentation**: Setup instructions, example prompts, screenshots

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud Project with Gmail API enabled
- OAuth2 credentials (not app passwords)
- Claude Desktop

### Gmail API Setup

1. Create Google Cloud Project
2. Enable Gmail API
3. Configure OAuth2 (scopes: gmail.readonly, gmail.compose)
4. Download credentials.json

### Claude Desktop Configuration

#### Step 1: Locate Your Config File

The config file location depends on your operating system:

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

#### Step 2: Add MCP Server Configuration

Add this to your `claude_desktop_config.json` file:

```json
{
  "mcpServers": {
    "gmail_mcp_server": {
      "command": "/Users/YOUR_USERNAME/path/to/gmail-mcp/.venv/bin/python",
      "args": ["/Users/YOUR_USERNAME/path/to/gmail-mcp/main.py"]
    }
  }
}
```

**Important**: Replace the paths with your actual absolute paths:

1. Find your project directory: `pwd` (when in the gmail-mcp directory)
2. Update both the `command` path (to Python in .venv) and `args` path (to main.py)

**Example (macOS)**:
```json
{
  "mcpServers": {
    "gmail_mcp_server": {
      "command": "/Users/johndoe/projects/gmail-mcp/.venv/bin/python",
      "args": ["/Users/johndoe/projects/gmail-mcp/main.py"]
    }
  }
}
```

**Example (Windows)**:
```json
{
  "mcpServers": {
    "gmail_mcp_server": {
      "command": "C:\\Users\\johndoe\\projects\\gmail-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\Users\\johndoe\\projects\\gmail-mcp\\main.py"]
    }
  }
}
```

#### Step 3: Restart and Authenticate

1. **Save** the config file
2. **Restart** Claude Desktop completely (quit and reopen)
3. **Verify connection**: Look for the 🔌 icon in Claude Desktop indicating MCP servers are connected
4. **First-time authentication**: On first use, a browser window will open asking you to:
   - Sign in to your Google account
   - Grant permissions for Gmail read and compose access
   - The server will save a `token.json` file in the `credentials/` directory

#### Troubleshooting

**Server not connecting?**
- Verify paths are absolute (not relative like `~/` or `./`)
- Check Python virtual environment is activated and dependencies installed
- Look at Claude Desktop logs: `~/Library/Logs/Claude/mcp*.log` (macOS)

**Authentication failing?**
- Ensure `credentials.json` is in the `credentials/` directory
- Delete `credentials/token.json` and retry to re-authenticate
- Verify Gmail API is enabled in Google Cloud Console
- Check OAuth scopes include `gmail.readonly` and `gmail.compose`

**Server crashes on startup?**
- Run manually to see errors: `.venv/bin/python main.py`
- Check all dependencies installed: `uv sync`

## Email Writing Guidelines (MCP Resources)

This server exposes comprehensive email writing guidelines as MCP resources. Claude can access these when drafting emails to ensure professional, consistent communication.

### Available Resources

Three resources are available at fixed URIs:

1. **`file:///email-guidelines/7cs-communication.md`** - The 7 Cs of Effective Communication
   - Framework for professional emails (Clarity, Conciseness, Correctness, Coherence, Completeness, Courtesy, Concreteness)
   - Ensures all emails meet professional standards

2. **`file:///email-guidelines/personal-templates.md`** - Personal Email Templates
   - 11 templates for common personal tasks (appointments, quotes, birthday wishes, neighbor communications, etc.)
   - Ready-to-use formats for everyday email scenarios

3. **`file:///email-guidelines/ai-drafting-directive.md`** - AI Email Drafting Directive
   - Comprehensive guidelines incorporating Dale Carnegie, Robert Cialdini, and Stephen Covey principles
   - Persona definition, tone mapping by category, ethical persuasion tactics

### How Resources Work

Claude Desktop automatically makes these resources available to Claude when the MCP server is connected. Claude can:

- **Access automatically** - Resources are discoverable through the MCP protocol
- **Reference when needed** - Claude can read resources to understand your email writing standards
- **Apply guidelines** - Use the 7 Cs framework and templates when drafting replies

### Using Resources

Simply ask Claude to draft emails - the resources are available automatically:

```
Draft a professional reply to this email about the budget review.
```

Or explicitly reference specific resources:

```
Draft a reply following the 7 Cs guidelines and use one of my personal templates if appropriate.
```

### Optional: Google Docs Integration

By default, resources are read from local markdown files in the `docs/` directory. You can optionally configure the server to fetch these from Google Docs instead.

**Why use Google Docs?**

- Centralized, shareable guidelines
- Update without modifying code
- Collaborate with team members
- Version history

**Setup:**

1. Upload your three guideline documents to Google Docs
2. Get document IDs from URLs: `https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit`
3. Configure in `src/gmail_mcp_server/configs/settings.toml`:
   ```toml
   [default.google_docs]
   7cs_doc_id = "YOUR_7CS_DOCUMENT_ID"
   templates_doc_id = "YOUR_TEMPLATES_DOCUMENT_ID"
   directive_doc_id = "YOUR_DIRECTIVE_DOCUMENT_ID"
   ```
4. Add Google Docs scope to settings.toml:
   ```toml
   google_scopes = [
       "https://www.googleapis.com/auth/calendar.calendarlist.readonly",
       "https://www.googleapis.com/auth/calendar.events.freebusy",
       "https://www.googleapis.com/auth/drive.readonly",
       "https://www.googleapis.com/auth/gmail.readonly",
       "https://www.googleapis.com/auth/gmail.compose"
   ]
   ```
5. Delete `credentials/token.json` and restart server to re-authenticate

**Fallback:** If Google Docs fetch fails, the server automatically falls back to local files.

## Local Development

### Setup

1. Clone the repository
2. Install dependencies: `uv install`
3. Configure your Gmail API credentials (see [docs/gcp-setup.md](docs/gcp-setup.md))
4. Run the server: `uv run gmail-mcp-server`

### Testing with MCP Inspector

For debugging and testing:

```bash
npx @modelcontextprotocol/inspector uv --directory /path/to/gmail-mcp run gmail-mcp-server
```

### Sample Prompts

#### Prompt 1: Read and Summarize Unread Emails

```
Show me my 3 most recent unread emails and provide a brief summary of each one, including who sent it and what it's about.
```

#### Prompt 2: Draft Reply with Guidelines

```
Check my unread emails. For the first one from Sarah, draft a professional reply using the 7 Cs guidelines.
I need to schedule a follow-up meeting to discuss Q4 budget and timeline.
```

#### Prompt 3: Use Personal Email Template

```
I got an appointment reminder from my dentist for next Tuesday at 3pm.
Draft a confirmation reply using one of my personal email templates.
```

#### Prompt 4: Draft Reply Following All Guidelines

```
Draft a reply to John's email using my AI drafting directive and the 7 Cs framework.
I need to apologize for the delayed report and explain it's now complete.
```

**Note**: After drafting, check your Gmail drafts folder to review before sending.

For more example prompts, see [docs/example-prompts.md](docs/example-prompts.md)

### Demo Video

Watch the Gmail MCP Server in action:

https://github.com/user-attachments/assets/demo_mcp.mov

The demo shows:
-  Getting unread emails from Gmail
-  Creating draft replies with threading

### Screenshots

#### MCP Server Connected in Claude Desktop
![MCP Server Connection](./screenshots/Screenshot%202025-12-15%20at%2014.33.55.png)

#### Fetching Unread Emails
![Getting Unread Emails](./screenshots/Screenshot%202025-12-15%20at%2014.35.10.png)

#### Drafting Professional Reply with 7 Cs Framework
![Draft Professional Reply](./screenshots/Screenshot%202025-12-15%20at%2015.05.32.png)

#### Using Personal Email Templates
![Email Templates](./screenshots/Screenshot%202025-12-15%20at%2015.06.38.png)

#### MCP Prompts in Action
![MCP Prompts](./screenshots/Screenshot%202025-12-15%20at%2015.19.27.png)

#### Draft Reply Created in Gmail
![Gmail Draft](./screenshots/Screenshot%202025-12-15%20at%2015.19.31.png)

## MCP Prompts

This server provides three sophisticated prompts that leverage advanced prompt engineering techniques:

### 1. `draft_professional_reply` - Multi-Step Chain + Role Prompting

**Purpose:** Generate professional email replies following the 7 Cs framework and your personal AI directive using chain of thought reasoning.

**Arguments:**
- `thread_id` (required): The email thread ID to reply to
- `key_points` (optional): Key points to include in the reply
- `tone` (optional): Desired tone - formal, professional, or friendly (default: professional)

**Prompt Engineering Technique:** Chain of Thought
- 7-step reasoning process from context retrieval to draft creation
- Applies consistent persona from AI directive
- Validates against 7 Cs checklist
- UK English formatting

**Example Usage:**
```
Use draft_professional_reply with thread_id="abc123", key_points="confirm meeting availability", tone="professional"
```

### 2. `schedule_meeting_reply` - Contextual + Calendar Integration

**Purpose:** Draft meeting acceptance or proposal with real-time calendar availability context.

**Arguments:**
- `thread_id` (required): The meeting request email thread ID
- `date_range_start` (required): Start date for availability check (ISO format: YYYY-MM-DD)
- `date_range_end` (required): End date for availability check (ISO format: YYYY-MM-DD)
- `proposed_times` (optional): Optional specific times to propose

**Prompt Engineering Technique:** Contextual Prompting
- Integrates live calendar availability data
- Enforces AI directive's "2 time slots" scheduling protocol
- UK date/time format with timezone (BST/GMT)
- Contextual reasoning based on meeting request

**Example Usage:**
```
Use schedule_meeting_reply with thread_id="xyz789", date_range_start="2025-12-16", date_range_end="2025-12-20"
```

### 3. `suggest_template` - Few-Shot Learning

**Purpose:** Analyze an email and suggest the most appropriate personal template from your collection of 11 templates.

**Arguments:**
- `thread_id` (required): The email thread ID to analyze

**Prompt Engineering Technique:** Few-Shot Learning
- Pattern matching against 11 personal templates
- Confidence scoring (0-100%)
- Explains reasoning for template selection
- Shows customization fields needed
- Provides populated template preview

**Example Usage:**
```
Use suggest_template with thread_id="def456"
```

### Resource Usage Matrix

| Prompt | 7 Cs Framework | Email Templates | AI Directive | Calendar Availability |
|--------|----------------|-----------------|--------------|----------------------|
| **draft_professional_reply** | ✅ Yes | ✅ Yes (optional) | ✅ Yes | ❌ No |
| **schedule_meeting_reply** | ✅ Yes | ❌ No | ✅ Yes | ✅ Yes |
| **suggest_template** | ❌ No | ✅ Yes | ❌ No | ❌ No |

**Summary:**
- All prompts access at least 2 resources
- `draft_professional_reply` uses 3 resources (7 Cs, AI directive, optionally templates)
- `schedule_meeting_reply` uses 3 resources (7 Cs, AI directive, calendar availability)
- `suggest_template` uses 1 primary resource (email templates)

## Project Status: 🧪 Testing

All core requirements and stretch goals have been successfully implemented and tested.
