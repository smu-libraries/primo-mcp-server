from __future__ import annotations

"""SMU Primo MCP Server -- search Singapore Management University Library."""

__version__ = "0.1.0"

import os
from typing import Final

from primo_mcp_server.server import asgi_app, mcp

DEFAULT_TRANSPORT: Final = "stdio"


def main() -> None:
    """Entry point for the primo-mcp-server command."""
    transport = os.getenv("PRIMO_MCP_TRANSPORT", os.getenv("MCP_TRANSPORT", DEFAULT_TRANSPORT)).strip().lower()
    if transport == "stdio":
        mcp.run(transport="stdio")
        return

    if transport == "streamable-http":
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", os.getenv("WEBSITES_PORT", "8000")))
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")
        return

    if transport == "sse":
        mcp.run(transport="sse")
        return

    raise ValueError(
        f"Unsupported transport: {transport!r}. "
        "Use PRIMO_MCP_TRANSPORT=stdio|streamable-http|sse."
    )
