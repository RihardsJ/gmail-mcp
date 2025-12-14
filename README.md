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

## Project Milestones

### Core Requirements

- [x] **Gmail API Setup**: Google Cloud project, OAuth2 configuration, scopes
- [x] **MCP Server**: Python implementation with mcp SDK
- [x] **Authorization**: OAuth2 authentication for Gmail API
- [x] **Email Retrieval Tool**: `get_unread_emails` with required fields
- [x] **Draft Reply Tool**: `create_draft_reply` with threading
- [x] **Claude Desktop Integration**: Local server configuration and testing
- [ ] **Documentation**: Setup instructions, example prompts, screenshots

### Stretch Goals

- [x] **Email Style Guide Integration**: Pull writing guidelines from Google Docs ✅
- [x] **Reply Templates**: Integrate templates from local files (with Google Docs support) ✅
- [x] **Knowledge Base Context**: Enhance replies with the 7 Cs framework and AI directive ✅
- [x] **MCP Resources**: Expose email guidelines as MCP resources ✅

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

Add this to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "gmail_mcp_server": {
      "command": "root_path_to/gmail-mcp/venv/bin/python",
      "args": ["root_path_to/gmail-mcp/main.py"]
    }
  }
}
```

**Important**: Replace `/absolute/path/to/gmail-mcp` with the actual path to your project directory.

After updating the config:
1. Save the file
2. Restart Claude Desktop
3. On first use, you'll be prompted to authenticate with Google OAuth

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
       "https://www.googleapis.com/auth/gmail.readonly",
       "https://www.googleapis.com/auth/gmail.compose",
       "https://www.googleapis.com/auth/documents.readonly"
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

📝 **Note**: After drafting, check your Gmail drafts folder to review before sending.

For more example prompts, see [docs/example-prompts.md](docs/example-prompts.md)

### Screenshots

Coming soon!

## Project status: 🧑‍💻 In development
