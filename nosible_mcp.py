# nosible_mcp.py
import os
from typing import Union

from config import settings
import traceback

# 1) Determine the key (settings, env, or hardcoded for dev)
API_KEY = (
    (settings.NOSIBLE_API_KEY or os.getenv("NOSIBLE_API_KEY") or "").strip()
)
if not API_KEY:
    raise RuntimeError("NOSIBLE_API_KEY not set")

# 2) Make it available BEFORE importing nosible (critical)
os.environ["NOSIBLE_API_KEY"] = API_KEY

# 3) Now import nosible and MCP
from nosible import Nosible, ResultSet
from mcp.server.fastmcp import FastMCP
import inspect, nosible as _nosible

# Debug prints once, so you can see what’s actually imported
print("Loaded nosible_mcp.py from:", __file__)
print("nosible file:", _nosible.__file__)
print("Nosible.__init__:", inspect.signature(Nosible))
print("NOSIBLE_API_KEY present at import?", bool(os.getenv("NOSIBLE_API_KEY")))

# Create an MCP server
mcp = FastMCP("search-dev-proof")

import nosible as _nosible, inspect, os, logging
print("nosible file:", _nosible.__file__)
print("Nosible.__init__:", inspect.signature(Nosible))
print("NOSIBLE_API_KEY present at import?", bool(os.getenv("NOSIBLE_API_KEY")))


# # Add a tool that uses NOSIBLE
# @mcp.tool()
# def search(query: str) -> Union[dict, any]:
#     """Make a search on the Nosible Search engine."""
#     try:
#         import logging, importlib
#         logging.warning("tool sees NOSIBLE_API_KEY? %s", bool(os.getenv("NOSIBLE_API_KEY")))
#         importlib.reload(_nosible)
#         from nosible import Nosible
#         api_key = settings.NOSIBLE_API_KEY or os.getenv("NOSIBLE_API_KEY")
#         if not api_key:
#             raise RuntimeError("NOSIBLE_API_KEY not set")
#
#         if not api_key:
#             raise RuntimeError("NOSIBLE_API_KEY not set")
#         with Nosible(nosible_api_key=api_key) as nos:
#             results = nos.fast_search(question=query, n_results=10)
#     except Exception as e:
#         return {
#             "error": str(e),
#             "trace": traceback.format_exc(limit=8)
#         }
#
#     results = results.to_dict()
#
#     return results

from typing import Any, Dict
from mcp.server.fastmcp import FastMCP
from nosible import Nosible

@mcp.tool(structured_output=False)   # <-- tell FastMCP not to model the output
def search(query: str) -> Dict[str, Any]:   # <-- JSON-friendly type
    """Make a search on the Nosible Search engine."""
    import os, logging, importlib, nosible as _nosible
    logging.warning("tool sees NOSIBLE_API_KEY? %s", bool(os.getenv("NOSIBLE_API_KEY")))
    importlib.reload(_nosible)  # safe against early import

    with Nosible() as nos:
        rs = nos.fast_search(question=query, n_results=10)

    # normalize to JSON-serializable dict
    if hasattr(rs, "to_dict"):
        return rs.to_dict()
    if hasattr(rs, "model_dump"):
        return rs.model_dump()
    # last-resort generic encoding
    from fastapi.encoders import jsonable_encoder
    return jsonable_encoder(rs, exclude_none=True)