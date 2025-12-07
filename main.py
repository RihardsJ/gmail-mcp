#!/usr/bin/env python3

import asyncio

import mcp.server.stdio

from .src.mcp_server import mcp_server


async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream, write_stream, mcp_server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
