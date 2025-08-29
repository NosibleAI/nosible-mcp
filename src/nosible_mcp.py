from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from context_keys import current_nosible_api_key

# MCP app; streamable HTTP endpoint will live at the mount path (see server.py)
mcp = FastMCP("nosible-demo", streamable_http_path="/")

def _get_key() -> str | dict:
    key =  current_nosible_api_key.get()
    if not key:
        return {
            "error": "missing_api_key",
            "message": "Provide X-Nosible-Api-Key header in client config."
        }
    else:
        return key

@mcp.tool()
def search(question: str, n_results: int = 10) -> dict:
    """
    Per-user Nosible search.

    The API key must be sent by the client in the HTTP header:
      X-Nosible-Api-Key: <key>

    Args:
      question: natural language search prompt
      n_results: number of results to return

    Returns:
      JSON-serializable dict representation of Nosible ResultSet.
    """
    # Lazy import keeps server startup instant
    from nosible import Nosible

    key = _get_key()
    try:
        # Prefer constructor param so we don't touch process-wide env
        with Nosible(nosible_api_key=key) as nos:
            rs = nos.fast_search(question=question, n_results=n_results)
            return rs.to_dict()

    except Exception as e:
        return {"error": str(e)}
