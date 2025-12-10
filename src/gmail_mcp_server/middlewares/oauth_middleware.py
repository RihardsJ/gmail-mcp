"""
OAuth 2.0 Middleware for MCP Server

This middleware implements the OAuth 2.0 authorization flow for MCP servers:
1. Initial 401 handshake with WWW-Authenticate header pointing to PRM document
2. Token validation for protected endpoints
3. Proper error handling with MCP-compliant responses
"""

from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    AuthenticationError,
    SimpleUser,
)
from starlette.requests import HTTPConnection, Request
from starlette.responses import JSONResponse, Response


class OAuthMiddleware(AuthenticationBackend):
    """
    OAuth middleware that implements MCP OAuth flow.

    On first connection without auth, returns 401 with WWW-Authenticate header
    pointing to the Protected Resource Metadata (PRM) document.
    """

    async def authenticate(self, conn: HTTPConnection):
        """
        Authenticate the request by checking for Bearer token.

        Args:
            conn: The HTTP connection object

        Returns:
            Tuple of (AuthCredentials, SimpleUser) if authenticated

        Raises:
            AuthenticationError: If authentication is required but token is invalid
        """
        # Skip authentication for public endpoints
        if conn.url.path in [
            "/health",
            "/oauth/authorize",
            "/oauth/callback",
            "/.well-known/oauth-protected-resource",
        ]:
            return

        # Check if Authorization header exists
        if "Authorization" not in conn.headers:
            # Return 401 with WWW-Authenticate header for MCP OAuth flow
            raise AuthenticationError("Authentication required")

        auth_header = conn.headers["Authorization"]

        try:
            # Split the auth header into scheme and token
            scheme, token = auth_header.split(None, 1)

            # Check if it's a Bearer token
            if scheme.lower() != "bearer":
                raise AuthenticationError(
                    "Invalid authentication scheme. Expected 'Bearer'"
                )

            if not token:
                raise AuthenticationError("Bearer token is empty")

            # TODO: Add actual token validation logic here
            # - Verify token with OAuth provider
            # - Check token expiry
            # - Extract user information from token
            # - Validate scopes

            # For now, accept any Bearer token
            return AuthCredentials(["authenticated"]), SimpleUser(username="oauth_user")

        except ValueError:
            # Couldn't split the header properly
            raise AuthenticationError("Invalid Authorization header format")


def handle_oauth_error(conn: HTTPConnection, exc: AuthenticationError) -> Response:
    """
    Custom error handler for authentication errors.
    Returns 401 with the MCP-specific WWW-Authenticate header.
    """
    # Construct the PRM document URL
    host = conn.headers.get("Host", "localhost:8100")
    scheme = "https" if conn.url.scheme == "https" else "http"
    prm_url = f"{scheme}://{host}/.well-known/oauth-protected-resource"

    return JSONResponse(
        {"error": str(exc), "message": "Authentication required"},
        status_code=401,
        headers={
            "WWW-Authenticate": f'Bearer realm="mcp", resource_metadata="{prm_url}"'
        },
    )
