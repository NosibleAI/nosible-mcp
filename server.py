# server.py
import contextlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from auth import AuthMiddleware
from nosible_mcp import mcp

# Create the Streamable HTTP sub-app and mount at /mcp
mcp_app = mcp.streamable_http_app()  # returns a Starlette app

@contextlib.asynccontextmanager
async def lifespan(_: FastAPI):
    async with mcp.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)

# CORS + expose session header (per MCP Streamable HTTP spec)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
    allow_methods=["*"],
    expose_headers=["Mcp-Session-Id"],
)

# OAuth protection
app.add_middleware(AuthMiddleware)

# OAuth 2.1 protected resource metadata (well-known)
@app.get("/.well-known/oauth-protected-resource/mcp")
def discovery():
    return {
        "authorization_servers": [settings.SCALEKIT_AUTHORIZATION_SERVERS],
        "bearer_methods_supported": ["header"],
        "resource": settings.SCALEKIT_RESOURCE_NAME,      # MUST match what you register in ScaleKit
        "resource_documentation": settings.SCALEKIT_RESOURCE_DOCS_URL,
        "scopes_supported": ["mcp:tools:search"],
    }

# Mount MCP app under /mcp/  (note the trailing slash discipline)
app.mount("/mcp", mcp_app)
