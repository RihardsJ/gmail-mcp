.PHONY: help run inspector docker-build docker-up docker-down docker-logs docker-restart clean

# Default target
help:
	@echo "Available commands:"
	@echo "  make run             - Run the server locally using uv"
	@echo "  make dev             - Run the server in development mode with auto-reload"
	@echo "  make inspector       - Run MCP Inspector"
	@echo "  make docker-build    - Build the Docker image"
	@echo "  make docker-up       - Start the Docker container"
	@echo "  make docker-down     - Stop the Docker container"
	@echo "  make docker-logs     - View Docker container logs"
	@echo "  make docker-restart  - Restart the Docker container"
	@echo "  make clean           - Remove Python cache files"

# Run locally
run:
	uv run python main.py

# Run in development mode with auto-reload
dev:
	uv run uvicorn main:app --factory --reload --host 0.0.0.0 --port 8100

# MCP Inspector
inspector:
	npx @modelcontextprotocol/inspector

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
