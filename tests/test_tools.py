# tests/test_tools.py
def test_fast_search_passes_expansions(import_server):
    srv = import_server
    # Call tool directly
    result = srv.fast_search(
        question="NVIDIA vs AMD",
        expansions=["NVIDIA AI roadmap", "AMD MI300X roadmap"],
        n_results=5,
    )
    assert "data" in result
    assert result["data"][0]["title"] == "ok"

def test_scrape_url_returns_payload(import_server):
    srv = import_server
    out = srv.scrape_url(url="https://example.com", render=False)
    assert out["page"]["title"] == "Example"
    assert "full_text" in out

def test_topic_trend_returns_mapping(import_server):
    srv = import_server
    out = srv.topic_trend(query="test", start_date="2025-01-01", end_date="2025-02-01")
    assert "2025-01-31" in out

# def test_generate_expansions_parses_json(import_server, fake_ctx_json):
#     srv = import_server
#     exps = srv.generate_expansions(fake_ctx_json, question="q", n=10)
#     assert len(exps) == 10
#     assert all(isinstance(x, str) and x for x in exps)
#
# def test_generate_expansions_handles_non_json_lines(import_server, fake_ctx_lines):
#     srv = import_server
#     exps = srv.generate_expansions(fake_ctx_lines, question="q", n=5)
#     # Should fall back to line parsing and de-dup
#     assert exps[:3] == ["alpha", "beta", "gamma"]
#     assert len(exps) == 5 or len(exps) == 3  # depends how many lines you provided
