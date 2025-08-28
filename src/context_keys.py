# src/context_keys.py
from contextvars import ContextVar

# Holds the API key for *this* HTTP request only
current_nosible_api_key: ContextVar[str | None] = ContextVar(
    "current_nosible_api_key", default=None
)
