.PHONY: help activate run inspector clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make activate        - Activate the virtual environment"
	@echo "  make inspector       - Run MCP Inspector"
	@echo "  make clean           - Remove Python cache files"

# Activate virtual environment
activate:
	python -m venv venv
	source venv/bin/activate

# MCP Inspector
inspector:
	npx @modelcontextprotocol/inspector

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
