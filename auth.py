# auth.py
import json, logging
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware

from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions

from config import settings

logger = logging.getLogger(__name__)
security = HTTPBearer()

scalekit_client = ScalekitClient(
    settings.SCALEKIT_ENVIRONMENT_URL,
    settings.SCALEKIT_CLIENT_ID,
    settings.SCALEKIT_CLIENT_SECRET,
)

WHITELIST_PREFIXES = (
    "/.well-known/",
)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Public discovery endpoint
        if any(request.url.path.startswith(p) for p in WHITELIST_PREFIXES):
            return await call_next(request)

        # Dev bypass (handy while wiring)
        if settings.ALLOW_DEV_NOAUTH:
            return await call_next(request)

        # Expect Bearer token from OAuth-capable clients (or via mcp-remote)
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"error": "unauthorized", "error_description": "Missing or invalid authorization header"},
                headers={
                    "WWW-Authenticate": f'Bearer realm="OAuth", resource_metadata="{settings.SCALEKIT_RESOURCE_NAME.rstrip("/").replace("/mcp","")}/.well-known/oauth-protected-resource/mcp"'
                },
            )

        token = auth_header.split(" ", 1)[1]

        # Optionally enforce scope when the request is a tools/call
        try:
            body = await request.body()
            payload = {}
            try:
                payload = json.loads(body.decode("utf-8")) if body else {}
            except Exception:
                payload = {}

            required_scopes = []
            if payload.get("method") == "tools/call":
                required_scopes = ["mcp:tools:search"]

            opts = TokenValidationOptions(
                issuer=settings.SCALEKIT_ENVIRONMENT_URL,
                audience=[settings.SCALEKIT_RESOURCE_NAME],
                required_scopes=required_scopes or None,
            )
            scalekit_client.validate_access_token(token, options=opts)
        except Exception:
            return JSONResponse(
                status_code=401,
                content={"error": "unauthorized", "error_description": "Token validation failed"},
            )

        return await call_next(request)
