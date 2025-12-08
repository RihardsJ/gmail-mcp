# Gmail MCP Server - Dockerfile
# Optimized for Python 3.14 with slim variant

# Build stage
FROM python:3.14-slim as builder

LABEL maintainer="rihardsj@pm.me"
LABEL description="Gmail MCP Server"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv for faster dependency management
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Runtime stage
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Copy installed dependencies from builder
COPY --from=builder --chown=mcpuser:mcpuser /app/.venv /app/.venv

# Copy application code
COPY --chown=mcpuser:mcpuser main.py ./
COPY --chown=mcpuser:mcpuser configs/ ./configs/
COPY --chown=mcpuser:mcpuser src/ ./src/

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    # Default configuration (can be overridden)
    DYNACONF_HOST=0.0.0.0 \
    DYNACONF_PORT=8200 \
    DYNACONF_LOG_LEVEL=info

# Create logs directory
RUN mkdir -p /app/logs && chown mcpuser:mcpuser /app/logs

# Expose port
EXPOSE 8200

# Switch to non-root user
USER mcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8200/health || exit 1

# Run the server
CMD ["python", "main.py"]
