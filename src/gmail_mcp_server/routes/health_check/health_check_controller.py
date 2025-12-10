from starlette.responses import JSONResponse


async def health_check_controller(request):
    """Health check controller for Docker and monitoring."""

    return JSONResponse(
        {
            "status": "healthy",
            "service": "gmail-mcp-server",
            "timestamp": str(__import__("datetime").datetime.now().isoformat()),
        }
    )
