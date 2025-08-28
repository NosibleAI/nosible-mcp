# src/nosible_mcp.py
from __future__ import annotations
from mcp.server.fastmcp import FastMCP
from typing import Optional
from context_keys import current_nosible_api_key

# MCP app; streamable HTTP endpoint will live at the mount path (see server.py)
mcp = FastMCP("nosible-demo", streamable_http_path="/")

def _get_key() -> Optional[str]:
    return current_nosible_api_key.get()

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
    key = _get_key()
    if not key:
        return {
            "error": "missing_api_key",
            "message": "Provide X-Nosible-Api-Key header in client config."
        }

    # Lazy import keeps server startup instant
    from nosible import Nosible

    try:
        # Prefer constructor param so we don't touch process-wide env
        with Nosible(nosible_api_key=key) as nos:
            rs = nos.fast_search(question=question, n_results=n_results)
            return rs.to_dict()
    # except TypeError:
    #     # Fallback if your nosible-py version doesn't accept api_key=...
    #     # (Simple but not concurrency-safe: avoid in multi-user production)
    #     import os
    #     old = os.environ.get("NOSIBLE_API_KEY")
    #     os.environ["NOSIBLE_API_KEY"] = key
    #     try:
    #         with Nosible() as nos:
    #             rs = nos.fast_search(question=question, n_results=n_results)
    #             return rs.to_dict()
    #     finally:
    #         if old is None:
    #             os.environ.pop("NOSIBLE_API_KEY", None)
    #         else:
    #             os.environ["NOSIBLE_API_KEY"] = old
    except Exception as e:
        return {"error": str(e)}
