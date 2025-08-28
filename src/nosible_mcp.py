# src/nosible_mcp.py
from __future__ import annotations
from mcp.server.fastmcp import FastMCP

# Create the MCP app. Using streamable_http_path="/"
# means the MCP endpoint will be the mount path (e.g., /mcp/).
mcp = FastMCP("nosible-demo", streamable_http_path="/")

@mcp.tool()
def search(question: str, n_results: int = 10) -> dict:
    """
    Search the Nosible engine (fast, single query).

    Args:
        question: natural-language query (e.g., "LLM inference cost optimizations 2025")
        n_results: number of results to return (default 10)

    Returns:
        A JSON-serializable dict representation of a Nosible ResultSet.
        (Clients can render this or post-process it with other tools.)
    """
    # Lazy import keeps server startup instant and avoids import-time network calls
    from nosible import Nosible

    try:
        # Nosible reads NOSIBLE_API_KEY from environment by default
        with Nosible() as nos:
            rs = nos.fast_search(question=question, n_results=n_results)
            return rs.to_dict()
    except Exception as e:
        # Keep errors JSON-serializable for MCP clients
        return {"error": str(e)}
