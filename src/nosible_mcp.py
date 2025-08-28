from mcp.server.fastmcp import FastMCP

from typing import Dict, List

from config import settings

# Create an MCP server
mcp = FastMCP("web-search", streamable_http_path="/")


# Add a tool that uses NOSIBLE
@mcp.tool()
def web_search_01(query: str) -> Dict:
    """
    Use Nosible to search the web for information.

    Args:
        query: The search query.

    Returns:
        The search results.
    """
    from nosible import Nosible
    try:
        with Nosible() as nos:
            results = nos.fast_search(question=query, n_results=10)
            return results.to_dict()
    except Exception as e:
        return {"error": str(e)}

