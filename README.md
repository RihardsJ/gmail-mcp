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
- [ ] **Authorization**: OAuth2 authentication for Gmail API
- [ ] **Email Retrieval Tool**: `get_unread_emails` with required fields
- [ ] **Draft Reply Tool**: `create_draft_reply` with threading
- [ ] **Claude Desktop Integration**: Local server configuration and testing
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

### Usage with Claude Desktop (streamable-http transport layer):

```json
{
  "mcpServers": {
    "gmail-mcp-server": {
      TODO: add instructions
    }
  }
}
```

## Example Usage

### Run server in container

1. Start mcp server: `docker-compose up -d`
2. Stop mcp server: `docker-compose down`
3. View logs: `docker-compose logs -f`
4. Start inspector (for debugging): `npx @modelcontextprotocol/inspector`

### Run local server

1. `source venv/bin/activate`
2. Install dependencies: `uv install`
3. Start server: `uv run python main.py`

### Sample Prompts

Coming soon!

### Screenshots

Coming soon!

## Project status: 🚧 Planning
