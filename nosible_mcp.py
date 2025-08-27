from mcp.server.fastmcp import FastMCP
from nosible import Nosible, ResultSet
from typing import Dict, List
import os
import logging

from config import settings

# Create an MCP server
mcp = FastMCP("web-search")


# Add a tool that uses NOSIBLE
@mcp.tool()
def search(query: str) -> ResultSet:
    """Make a search on the Nosible Search engine."""
    api_key = settings.NOSIBLE_API_KEY or os.getenv("NOSIBLE_API_KEY")
    if not api_key:
        raise RuntimeError("NOSIBLE_API_KEY not set")
    with Nosible(nosible_api_key=api_key) as nos:
        results = nos.fast_search(question=query, n_results=10)

    return results