# src/server.py
from __future__ import annotations
import contextlib
import os
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

# Load .env for PORT, etc.
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:
    pass

from context_keys import current_nosible_api_key
from nosible_mcp import mcp as nosible_mcp_app

PORT = int(os.getenv("PORT", "10000"))

class PerUserKeyMiddleware(BaseHTTPMiddleware):
    """
    Pull 'X-Nosible-Api-Key' from the incoming request and stash it
    in a ContextVar so tools can read it for *this* call only.
    """
    async def dispatch(self, request: Request, call_next):
        key = (
            request.headers.get("X-Nosible-Api-Key")
            or request.headers.get("X-NOSIBLE-API-KEY")
        )
        token = current_nosible_api_key.set(key)
        try:
            return await call_next(request)
        finally:
            current_nosible_api_key.reset(token)

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    # manage MCP session manager lifecycle
    async with nosible_mcp_app.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)

# CORS (wide open for local dev; tighten for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],
)

# Install the per-user key middleware
app.add_middleware(PerUserKeyMiddleware)

# Optional health check
@app.get("/healthz")
def healthz():
    return {"ok": True}

# Mount the MCP streamable HTTP endpoint at /mcp/
mcp_http = nosible_mcp_app.streamable_http_app()
app.mount("/mcp", mcp_http)  # final endpoint: http://127.0.0.1:10000/mcp/

def main():
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")

if __name__ == "__main__":
    main()
