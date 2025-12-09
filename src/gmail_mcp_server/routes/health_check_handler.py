from starlette.responses import JSONResponse


async def health_check_handler(request):
    """Health check endpoint for Docker and monitoring."""
    return JSONResponse(
        {
            "status": "healthy",
            "service": "gmail-mcp-server",
            "timestamp": str(__import__("datetime").datetime.now().isoformat()),
        }
    )
