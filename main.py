import logging
import os

from mcp.server.fastmcp import FastMCP
from nosible import Nosible, ResultSet

# Initialize FastMCP server
mcp = FastMCP("nosible-mcp", host="127.0.0.1", port=8000)


@mcp.tool()
def search(query: str) -> ResultSet:
    """Make a search on the Nosible Search engine."""
    api_key = os.getenv("NOSIBLE_API_KEY")
    logging.info(("API key: ", api_key))
    with Nosible(nosible_api_key=api_key) as nos:
        results = nos.fast_search(question=query, n_results=10)

    return results


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="streamable-http")