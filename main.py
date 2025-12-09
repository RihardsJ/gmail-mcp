#!/usr/bin/env python3
"""
Gmail MCP Server - Low-Level Implementation with Streamable HTTP Transport

This server uses the low-level MCP Server API with manual ASGI setup.
Run with: python main.py or uv run python main.py
"""

import logging
from typing import Any

import mcp.types as types
import uvicorn
from mcp.server.lowlevel import Server
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.gmail_mcp_server.configs import configs
from src.gmail_mcp_server.middlewares import OAuthMiddleware, handle_oauth_error
from src.gmail_mcp_server.routes import (
    auth_handler,
    health_check_handler,
    oauth_protected_resource_handler,
)
from src.gmail_mcp_server.utils import print_terminal_banner

# Configure logging to suppress harmless cleanup errors in stateless mode
logging.getLogger("mcp.server.streamable_http").setLevel(logging.CRITICAL)

# Create low-level server instance
server = Server(configs.get("server_name", "gmail-mcp-server"))


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.

    This is called when a client requests the list of available tools.
    """
    return [
        types.Tool(
            name="hello",
            description="A simple hello tool to test the server",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Name to greet",
                        "default": "World",
                    }
                },
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent]:
    """
    Handle tool execution.

    This is called when a client wants to execute a tool.
    """
    if name == "hello":
        # Get the name argument, default to "World"
        user_name = (arguments or {}).get("name", "World")

        return [
            types.TextContent(
                type="text",
                text=f"Hello, {user_name}!",
            )
        ]
    else:
        raise ValueError(f"Unknown tool: {name}")


def create_app() -> Starlette:
    """
    Create the Starlette ASGI application with the MCP server mounted.
    """
    from contextlib import asynccontextmanager

    from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    from starlette.routing import Mount, Route

    # Create session manager for streamable HTTP
    session_manager = StreamableHTTPSessionManager(
        app=server,
        # Return JSON responses instead of SSE (better for Inspector)
        json_response=True,
        # Use stateless mode for scalability
        stateless=True,
    )

    @asynccontextmanager
    async def lifespan(app: Starlette):
        """Manage the session manager lifecycle."""
        async with session_manager.run():
            yield

    # Create the Starlette app with CORS support
    # Mount the session manager directly at root since it handles all MCP endpoints
    app = Starlette(
        routes=[
            Route("/health", health_check_handler, methods=["GET"]),
            Route("/auth", auth_handler, methods=["GET"]),
            Route(
                "/.well-known/oauth-protected-resource",
                oauth_protected_resource_handler,
                methods=["GET"],
            ),
            Mount("/", app=session_manager.handle_request),
        ],
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],  # Configure appropriately for production
                allow_credentials=True,
                allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
                allow_headers=["*"],
                expose_headers=["Mcp-Session-Id"],  # Required for MCP Inspector
            ),
            Middleware(
                AuthenticationMiddleware,
                backend=OAuthMiddleware(),
                on_error=handle_oauth_error,
            ),
        ],
        lifespan=lifespan,
    )

    return app


def app() -> Starlette:
    """
    Factory function for uvicorn --factory mode.

    This allows uvicorn to reload the app when files change in dev mode.
    Usage: uvicorn main:app --factory --reload
    """

    host = configs.get("host", "0.0.0.0")
    port = configs.get("port", 8100)
    print_terminal_banner(port, host)
    return create_app()


def main():
    """Run the server with uvicorn."""

    # Configuration from settings (supports environment variable overrides)
    host = configs.get("host", "0.0.0.0")
    port = configs.get("port", 8100)
    log_level = configs.get("log_level", "info")
    application = create_app()

    print_terminal_banner(port, host)

    # Run with uvicorn
    uvicorn.run(
        application,
        host=host,
        port=port,
        log_level=log_level,
    )


if __name__ == "__main__":
    main()
