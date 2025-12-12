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

## Core MCP Tools

- **`get_unread_emails`**: Returns sender, subject, body/snippet, and email/thread ID
- **`create_draft_reply`**: Creates correctly threaded draft replies from original email/thread ID and reply body

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

- [ ] **Email Style Guide Integration**: Pull writing guidelines from Google Docs
- [ ] **Reply Templates**: Integrate templates from Notion or local files
- [ ] **Knowledge Base Context**: Enhance replies with relevant company/personal context
- [ ] **Smart Reply Suggestions**: AI-powered reply recommendations based on email content

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

#### Prompt 2: Create Draft Reply
```
Check my unread emails. For the first one, draft a professional reply thanking the sender and saying I'll get back to them by end of week. Keep it friendly and concise.
```

📝 **Note**: After using Prompt 2, check your Gmail drafts folder to review the generated reply before sending.

For more example prompts, see [docs/example-prompts.md](docs/example-prompts.md).

### Screenshots

Coming soon!

## Project status: 🧑‍💻 In development
