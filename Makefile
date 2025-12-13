.PHONY: help activate run inspector clean test test-coverage test-watch test-verbose clean-test install-hooks

# Default target
help:
	@echo "Available commands:"
	@echo "  make activate        - Activate the virtual environment"
	@echo "  make inspector       - Run MCP Inspector"
	@echo "  make clean           - Remove Python cache files"
	@echo "  make settings        - Show command and argument values"
	@echo ""
	@echo "Testing commands:"
	@echo "  make test            - Run all tests"
	@echo "  make test-coverage   - Run tests with coverage report"
	@echo "  make test-verbose    - Run tests with verbose output"
	@echo "  make test-watch      - Run tests in watch mode (re-run on changes)"
	@echo "  make clean-test      - Remove test cache and coverage files"
	@echo ""
	@echo "Git hooks:"
	@echo "  make install-hooks   - Install git hooks (pre-push tests)"

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
	@echo "      \"args\": [\"$(PWD)/main.py\"]"
	@echo "    }"
	@echo "  }"
	@echo "}"

# Testing
test:
	uv run pytest

test-coverage:
	uv run pytest --cov=src/gmail_mcp_server --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

test-verbose:
	uv run pytest -v

test-watch:
	uv run pytest-watch

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 3>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

clean-test:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -f .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Git hooks
install-hooks:
	@echo "Installing git hooks..."
	@mkdir -p .git/hooks
	@cp .githooks/pre-push .git/hooks/pre-push
	@chmod +x .git/hooks/pre-push
	@echo "✅ Pre-push hook installed successfully!"
	@echo ""
	@echo "Tests will now run automatically before each push."
	@echo "To skip the hook, use: git push --no-verify"
