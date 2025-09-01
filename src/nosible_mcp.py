from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from context_keys import current_nosible_api_key

# MCP app; streamable HTTP endpoint will live at the mount path (see server.py)
mcp = FastMCP("nosible-demo", streamable_http_path="/")


def _get_key() -> str | dict:
    key =  current_nosible_api_key.get()
    if not key:
        return {
            "error": "missing_api_key",
            "message": "Provide X-Nosible-Api-Key header in client config."
        }
    else:
        return key


@mcp.tool(name="fast-search")
def fast_search(
    question: str,
    expansions: list[str] = None,
    n_results: int = 100,
    n_probes: int = 30,
    n_contextify: int = 128,
    algorithm: str = "hybrid-3",
    min_similarity: float = None,
    must_include: list[str] = None,
    must_exclude: list[str] = None,
    autogenerate_expansions: bool = False,
    publish_start: str = None,
    publish_end: str = None,
    include_netlocs: list = None,
    exclude_netlocs: list = None,
    visited_start: str = None,
    visited_end: str = None,
    certain: bool = None,
    include_companies: list = None,
    exclude_companies: list = None,
    include_docs: list = None,
    exclude_docs: list = None,
    brand_safety: str = None,
    language: str = None,
    continent: str = None,
    region: str = None,
    country: str = None,
    sector: str = None,
    industry_group: str = None,
    industry: str = None,
    sub_industry: str = None,
    iab_tier_1: str = None,
    iab_tier_2: str = None,
    iab_tier_3: str = None,
    iab_tier_4: str = None,
    instruction: str = None,
) -> dict:
    """
    Run a web search using the NOSIBLE search engine.

    Parameters
    ----------
    question : str
        Query string.
    expansions : list of str, optional
        Up to 10 semantically/lexically related queries to boost recall.
    n_results : int
        Max number of results (max 100).
    n_probes : int
        Number of index shards to probe.
        More shards will mean better recall, but slower query speeds.
    n_contextify : int
        Context window size per result.
    algorithm : str
        Search algorithm type.
    min_similarity : float
        Results must have at least this similarity score.
    must_include : list of str
        Only results mentioning these strings will be included.
    must_exclude : list of str
        Any result mentioning these strings will be excluded.
    autogenerate_expansions : bool
        Do you want to generate expansions automatically using a LLM?
    publish_start : str, optional
        Start date for when the document was published (ISO format).
    publish_end : str, optional
        End date for when the document was published (ISO format).
    visited_start : str, optional
        Start date for when the document was visited by NOSIBLE (ISO format).
    visited_end : str, optional
        End date for when the document was visited by NOSIBLE (ISO format).
    certain : bool, optional
        Only include documents where we are 100% sure of the date.
    include_netlocs : list of str, optional
        List of netlocs (domains) to include in the search. (Max: 50)
    exclude_netlocs : list of str, optional
        List of netlocs (domains) to exclude in the search. (Max: 50)
    include_companies : list of str, optional
        Google KG IDs of public companies to require (Max: 50).
    exclude_companies : list of str, optional
        Google KG IDs of public companies to forbid (Max: 50).
    include_docs : list of str, optional
        URL hashes of docs to include (Max: 50).
    exclude_docs : list of str, optional
        URL hashes of docs to exclude (Max: 50).
    brand_safety : str, optional
        Whether it is safe, sensitive, or unsafe to advertise on this content.
    language : str, optional
        Language code to use in search (ISO 639-1 language code).
    continent : str, optional
        Continent the results must come from (e.g., "Europe", "Asia").
    region : str, optional
        Region or subcontinent the results must come from (e.g., "Southern Africa", "Caribbean").
    country : str, optional
        Country the results must come from.
    sector : str, optional
        Sector the results must relate to (e.g., "Energy", "Information Technology").
    industry_group : str, optional
        Industry group the results must relate to (e.g., "Automobiles & Components", "Insurance").
    industry : str, optional
        Industry the results must relate to (e.g., "Consumer Finance", "Passenger Airlines").
    sub_industry : str, optional
        Sub-industry classification of the content's subject.
    iab_tier_1 : str, optional
        IAB Tier 1 category for the content.
    iab_tier_2 : str, optional
        IAB Tier 2 category for the content.
    iab_tier_3 : str, optional
        IAB Tier 3 category for the content.
    iab_tier_4 : str, optional
        IAB Tier 4 category for the content.
    instruction : str, optional
        Instruction to use with the search query.

    Returns
    -------
    JSON-serializable dict representation of Nosible ResultSet.
    """
    # Lazy import keeps server startup instant
    from nosible import Nosible

    key = _get_key()
    try:
        # Prefer constructor param so we don't touch process-wide env
        with Nosible(nosible_api_key=key) as nos:
            rs = nos.fast_search(
                question=question,
                expansions=expansions,
                n_results=n_results,
                n_probes=n_probes,
                n_contextify=n_contextify,
                algorithm=algorithm,
                min_similarity=min_similarity,
                must_include=must_include,
                must_exclude=must_exclude,
                autogenerate_expansions=autogenerate_expansions,
                publish_start=publish_start,
                publish_end=publish_end,
                include_netlocs=include_netlocs,
                exclude_netlocs=exclude_netlocs,
                visited_start=visited_start,
                visited_end=visited_end,
                certain=certain,
                include_companies=include_companies,
                exclude_companies=exclude_companies,
                include_docs=include_docs,
                exclude_docs=exclude_docs,
                brand_safety=brand_safety,
                language=language,
                continent=continent,
                region=region,
                country=country,
                sector=sector,
                industry_group=industry_group,
                industry=industry,
                sub_industry=sub_industry,
                iab_tier_1=iab_tier_1,
                iab_tier_2=iab_tier_2,
                iab_tier_3=iab_tier_3,
                iab_tier_4=iab_tier_4,
                instruction=instruction,
            )
            return rs.to_dict()

    except Exception as e:
        return {"error": str(e)}


@mcp.tool(name="scrape-url")
def scrape_url(
    html: str = "",
    recrawl: bool = False,
    render: bool = False,
    url: str = None
) -> str:
    """
    Scrape a given URL and return a structured WebPageData object for the page.

    Parameters
    ----------
    html : str
        Raw HTML to process instead of fetching.
    recrawl : bool
        If True, force a fresh crawl.
    render : bool
        If True, allow JavaScript rendering before extraction.
    url : str
        The URL to fetch and parse.

    Returns
    -------
    str
        Structured page data object.
    """

