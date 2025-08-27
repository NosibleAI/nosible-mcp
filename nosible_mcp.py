# nosible_mcp.py
import os, inspect
from typing import Dict, Any

from config import settings

# Make key available before importing nosible
if settings.NOSIBLE_API_KEY and not os.getenv("NOSIBLE_API_KEY"):
    os.environ["NOSIBLE_API_KEY"] = settings.NOSIBLE_API_KEY

from nosible import Nosible
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nosible-search")

@mcp.tool(structured_output=False)
def search(query: str) -> Dict[str, Any]:
    """
    Search the web via Nosible.
    The Nosible client accepts `nosible_api_key=...`.
    """
    api_key = os.getenv("NOSIBLE_API_KEY")  # you can also pass per-user keys inside the request if you build that flow
    if not api_key:
        raise RuntimeError("NOSIBLE_API_KEY not set")

    with Nosible(nosible_api_key=api_key) as nos:
        rs = nos.fast_search(question=query, n_results=10)

    return rs.to_dict() if hasattr(rs, "to_dict") else {"results": rs}
