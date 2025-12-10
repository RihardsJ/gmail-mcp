.PHONY: help activate run inspector clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make activate        - Activate the virtual environment"
	@echo "  make inspector       - Run MCP Inspector"
	@echo "  make clean           - Remove Python cache files"
	@echo "  make settings        - Show command and argument values"

# Activate virtual environment
activate:
	python -m venv venv
	source venv/bin/activate

# MCP Inspector
inspector:
	npx @modelcontextprotocol/inspector

# Settings (command and argument)
settings:
	@echo "{"
	@echo "  \"mcpServers\": {"
	@echo "    \"gmail_mcp_server\": {"
	@echo "      \"command\": \"$(PWD)/venv/bin/python\","
	@echo "      \"args\": [\"$(PWD)/email_server.py\"]"
	@echo "    }"
	@echo "  }"
	@echo "}"

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 3>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
