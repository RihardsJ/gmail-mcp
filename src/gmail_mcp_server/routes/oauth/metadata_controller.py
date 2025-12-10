from starlette.requests import Request
from starlette.responses import JSONResponse


async def oauth_metadata_controller(request: Request):
    issuer = "http://localhost:8100/oauth"
    metadata = {
        "issuer": issuer,
        "authorization_endpoint": issuer + "/authorize",
        "token_endpoint": issuer + "/token",
        "response_types_supported": ["code"],
    }
    return JSONResponse(metadata)
