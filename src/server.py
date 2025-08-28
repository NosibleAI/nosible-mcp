# src/server.py
import contextlib
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Load .env early (optional—but helpful in dev)
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except Exception:
    pass

from nosible_mcp import mcp as nosible_mcp_app

PORT = int(os.getenv("PORT", "10000"))

# Manage MCP session manager lifecycle
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with nosible_mcp_app.session_manager.run():
        yield

app = FastAPI(lifespan=lifespan)

# CORS: wide-open for local testing; tighten in prod
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Mcp-Session-Id"],  # helpful for streamable HTTP clients
)

# Optional health check (unauthenticated)
@app.get("/healthz")
def healthz():
    return {"ok": True}

# Mount the Streamable HTTP MCP endpoint
# With streamable_http_path="/", the endpoint lives at the mount root.
mcp_http = nosible_mcp_app.streamable_http_app()
app.mount("/mcp", mcp_http)  # final endpoint: http://localhost:10000/mcp/

def main():
    # Bind to IPv4 explicitly on Windows to avoid odd localhost/IPv6 issues
    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="info")

if __name__ == "__main__":
    main()
