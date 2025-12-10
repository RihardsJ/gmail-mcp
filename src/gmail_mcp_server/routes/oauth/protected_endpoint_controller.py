"""
OAuth Protected Resource Metadata Handler

This endpoint serves the Protected Resource Metadata (PRM) document
as specified in RFC 9728 Section 3.2.

The PRM document tells OAuth clients:
1. The resource identifier (this MCP server)
2. Which authorization servers can be used
3. What scopes are supported for this resource
"""

from starlette.requests import Request
from starlette.responses import JSONResponse


def oauth_protected_resource_controller(request: Request) -> JSONResponse:
    """
    Serves the Protected Resource Metadata (PRM) document.

    This endpoint is discovered via the WWW-Authenticate header's
    resource_metadata parameter during the initial 401 handshake.

    Returns:
        JSONResponse containing the PRM document with:
        - resource: The MCP server resource identifier
        - authorization_servers: List of OAuth authorization server URLs
        - scopes_supported: List of scopes this resource supports
    """
    scheme = "https" if request.url.scheme == "https" else "http"
    host = request.headers.get("Host", "localhost:8100")
    base_url = f"{scheme}://{host}"

    prm_document = {
        "resource": f"{base_url}/mcp",
        "authorization_servers": [f"{base_url}/auth"],
        "scopes_supported": [
            "mcp:tools",
            "mcp:resources",
            "mcp:prompts",
        ],
    }

    return JSONResponse(
        prm_document,
        status_code=200,
        headers={
            "Content-Type": "application/json",
        },
    )
