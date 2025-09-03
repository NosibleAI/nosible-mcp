# tests/conftest.py
import importlib
import importlib.util
import os
import sys
import types
from pathlib import Path

import pytest

# Make repo root and src/ importable (Windows-safe)
ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT, ROOT / "src"):
    s = str(p)
    if s not in sys.path:
        sys.path.insert(0, s)

# ------------------ Fakes ------------------

class _FakeResult:
    def __init__(self, payload): self._payload = payload
    def to_dict(self): return self._payload

class FakeNosible:
    """Stand-in for nosible.Nosible used by your tools."""
    def __init__(self, nosible_api_key: str): self.key = nosible_api_key
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): return False
    def fast_search(self, **kwargs):
        return _FakeResult({"data": [{"url": "https://example.com", "title": "ok"}]})
    def scrape_url(self, **kwargs):
        return _FakeResult({"page": {"title": "Example"}, "full_text": "hello"})
    def topic_trend(self, **kwargs):
        return {"2025-01-01": 5, "2025-01-31": 9}

class FakeCtx:
    """MCP Context stub with .sample()."""
    def __init__(self, text): self._text = text
    def sample(self, system_prompt: str, user_prompt: str, temperature: float = 0.3):
        return self._text

# -------------- Import helpers -------------

def _import_by_file(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, str(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def _scan_for_server():
    SKIP = {".venv", "venv", ".git", ".pytest_cache", ".ruff_cache", "__pycache__", "tests"}
    for base in (ROOT, ROOT / "src"):
        if not base.exists():
            continue
        for path in base.rglob("*.py"):
            if any(part in SKIP for part in path.parts):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if "FastMCP(" in text and "@mcp.tool" in text:
                return path
    return None

# -------------- Main fixture ---------------

@pytest.fixture
def import_server(monkeypatch):
    """
    Import your MCP server while forcing a fake `nosible` and stubbing `_get_key()`.
    Honors SERVER_MODULE or SERVER_FILE; otherwise auto-detects a file containing
    both `FastMCP(` and `@mcp.tool`.
    """
    # 1) Ensure fake `nosible` is used during import
    sys.modules["nosible"] = types.SimpleNamespace(Nosible=FakeNosible)

    # 2) Import the server module
    modname = os.getenv("SERVER_MODULE")
    modfile = os.getenv("SERVER_FILE")

    if modname:
        if modname in sys.modules:
            del sys.modules[modname]
        mod = importlib.import_module(modname)
    elif modfile:
        path = Path(modfile).resolve()
        if not path.exists():
            raise FileNotFoundError(f"SERVER_FILE not found: {path}")
        mod = _import_by_file(path)
    else:
        found = _scan_for_server()
        if not found:
            raise ModuleNotFoundError(
                "Could not locate your MCP server. Set SERVER_MODULE (e.g. 'nosible_mcp') "
                "or SERVER_FILE (full path), or ensure the file has FastMCP( ) and @mcp.tool."
            )
        mod = _import_by_file(found)

    # 3) Stub key retrieval so tests don't require real context
    if hasattr(mod, "_get_key"):
        monkeypatch.setattr(mod, "_get_key", lambda: "test-key", raising=True)

    return mod

# ----------- Context fixtures for tests -----

@pytest.fixture
def fake_ctx_json():
    return FakeCtx('["one","two","three","four","five","six","seven","eight","nine","ten"]')

@pytest.fixture
def fake_ctx_lines():
    return FakeCtx("- alpha\n- beta\n- gamma\n- delta\n- epsilon\n")
