from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from context_keys import current_nosible_api_key

from fastmcp import Context as ctx

# MCP app; streamable HTTP endpoint will live at the mount path (see server.py)
mcp = FastMCP("nosible-demo", streamable_http_path="/")


def _get_key() -> str:
    key =  current_nosible_api_key.get()
    if not key:
        raise ValueError("missing_api_key: Provide X-Nosible-Api-Key header in client config.")
    else:
        return key


@mcp.tool(name="fast-search")
async def fast_search(
    question: str,
    expansions: list[str] = None,
    n_results: int = 100,
    n_probes: int = 30,
    n_contextify: int = 128,
    algorithm: str = "hybrid-3",
    min_similarity: float = None,
    must_include: list[str] = None,
    must_exclude: list[str] = None,
    publish_start: str = None,
    publish_end: str = None,
    include_netlocs: list = None,
    exclude_netlocs: list = None,
    visited_start: str = None,
    visited_end: str = None,
    certain: bool = None,
    include_companies: list = None,
    exclude_companies: list = None,
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
    Run a web search using the NOSIBLE search engine. It is highly recommended to use
    expansions to boost recall, along with your search.

    Parameters
    ----------
    question : str
        Query string.
    expansions : list of str
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
    publish_start : str
        Start date for when the document was published (ISO format).
    publish_end : str
        End date for when the document was published (ISO format).
    visited_start : str
        Start date for when the document was visited by NOSIBLE (ISO format).
    visited_end : str
        End date for when the document was visited by NOSIBLE (ISO format).
    certain : bool
        Only include documents where we are 100% sure of the date.
    include_netlocs : list of str
        List of netlocs (domains) to include in the search. (Max: 50)
    exclude_netlocs : list of str
        List of netlocs (domains) to exclude in the search. (Max: 50)
    include_companies : list of str
        Google KG IDs of public companies to require (Max: 50).
    exclude_companies : list of str
        Google KG IDs of public companies to forbid (Max: 50).
    brand_safety : str
        Whether it is safe, sensitive, or unsafe to advertise on this content.
    language : str
        Language code to use in search (ISO 639-1 language code).
    continent : str
        Continent the results must come from (e.g., "Europe", "Asia").
    region : str
        Region or subcontinent the results must come from (e.g., "Southern Africa", "Caribbean").
    country : str
        Country the results must come from.
    sector : str
        Sector the results must relate to (e.g., "Energy", "Information Technology").
    industry_group : str
        Industry group the results must relate to (e.g., "Automobiles & Components", "Insurance").
    industry : str
        Industry the results must relate to (e.g., "Consumer Finance", "Passenger Airlines").
    sub_industry : str
        Sub-industry classification of the content's subject.
    iab_tier_1 : str
        IAB Tier 1 category for the content.
    iab_tier_2 : str
        IAB Tier 2 category for the content.
    iab_tier_3 : str
        IAB Tier 3 category for the content.
    iab_tier_4 : str
        IAB Tier 4 category for the content.
    instruction : str
        Instruction to use with the search query.

    Returns
    -------
    JSON-serializable dict representation of Nosible ResultSet that contains
    (e.g. data.url gives the url of the result):

    url : str
        The URL of the search result.
    title : str
        The title of the search result.
    description : str
        A brief description or summary of the search result.
    netloc : str
        The network location (domain) of the URL.
    published : str
        The publication date of the search result.
    visited : str
        The date and time when the result was visited.
    author : str
        The author of the content.
    content : str
        The main content or body of the search result.
    language : str
        The language code of the content (e.g., ‘en’ for English).
    similarity : float
        Similarity score with respect to a query or reference.
    brand_safety : str
        Whether it is safe, sensitive, or unsafe to advertise on this content.
    language : str
        Language code to use in search (ISO 639-1 language code e.g. "en").
    continent : str
        Continent the results must come from (e.g., “Europe”, “Asia”).
    region : str
        Region or subcontinent the results must come from (e.g., “Southern Africa”, “Caribbean”).
    country : str
        Country the results must come from.
    sector : str
        GICS Sector the results must relate to (e.g., “Energy”, “Information Technology”).
    industry_group : str
        GICS Industry group the results must relate to (e.g., “Automobiles & Components”, “Insurance”).
    industry : str
        GICS Industry the results must relate to (e.g., “Consumer Finance”, “Passenger Airlines”).
    sub_industry : str
        GICS Sub-industry classification of the content’s subject.
    iab_tier_1 : str
        IAB Tier 1 category for the content.
    iab_tier_2 : str
        IAB Tier 2 category for the content.
    iab_tier_3 : str
        IAB Tier 3 category for the content.
    iab_tier_4 : str
        IAB Tier 4 category for the content.

    Examples
    --------
    {
      "question": "European badger habitat",
        "expansions": [
            "European badger habitat requirements",
            "Meles meles living environment",
            "badger burrow habitat",
            "European badger woodland habitat",
            "badger sett location",
            "European badger geographic range",
            "badger habitat destruction",
            "European badger conservation habitat"
        ],
      "n_results": 100,
    }
    """
    import json

    # 1) If needed, ask the *client LLM* for expansions
    if not expansions:
        prompt = f"""
        # TASK DESCRIPTION

        Given a search question you must generate a list of 10 similar questions that have the same exact
        semantic meaning but are contextually and lexically different to improve search recall.

        ## Question

        Here is the question you must generate expansions for and the subject that it relates to:

        Question: {question}

        # RESPONSE FORMAT

        Your response must be a JSON object structured as follows: a list of ten strings. Each string must
        be a grammatically correct question that expands on the original question to improve recall.

        [
            string,
            string,
            string,
            string,
            string,
            string,
            string,
            string,
            string,
            string
        ]

        # EXPANSION GUIDELINES

        1. **Use specific named entities** - To improve the quality of your search results you must mention
           specific named entities (people, locations, organizations, products, places) in expansions.

        2. **Expansions must be highly targeted** - To improve the quality of search results each expansion
           must be semantically unambiguous. Questions must be use between ten and fifteen words.

        3. **Expansions must improve recall** - When expanding the question leverage semantic and contextual
           expansion to maximize the ability of the search engine to find semantically relevant documents:

           - Semantic Example: Swap "climate change" with "global warming" or "environmental change".
           - Contextual Example: Swap "diabetes treatment" with "insulin therapy" or "blood sugar management".

        """.replace("                ", "")

        try:
            resp = await ctx.sample(
                messages=prompt,
                system_prompt="You generate search query expansions. Output strict JSON only.",
                temperature=0.6,
                max_tokens=400,
                # Prefer fast/general models; client chooses the closest available one.
                model_preferences={"speedPriority": 0.7, "costPriority": 0.5, "intelligencePriority": 0.5},
            )  # ctx.sample is the server-side API to request client LLM sampling. :contentReference[oaicite:1]{index=1}
            data = json.loads(resp.text)
            expansions = [s.strip() for s in data.get("expansions", []) if isinstance(s, str)]
        except Exception:
            # Fallback: proceed without expansions if sampling or JSON parse fails
            expansions = []

        # Light cleanup & cap at 10
        uniq = []
        seen = set()
        for q in expansions:
            if q and q.lower() != question.lower() and q not in seen:
                uniq.append(q)
                seen.add(q)
            if len(uniq) >= 10:
                break
        expansions = uniq





    # Lazy import keeps server startup instant
    from nosible import Nosible

    key = _get_key()
    try:
        # Prefer constructor param so we don't touch process-wide env
        with Nosible(nosible_api_key=key) as nos:
            result = nos.fast_search(
                question=question,
                expansions=expansions,
                n_results=n_results,
                n_probes=n_probes,
                n_contextify=n_contextify,
                algorithm=algorithm,
                min_similarity=min_similarity,
                must_include=must_include,
                must_exclude=must_exclude,
                publish_start=publish_start,
                publish_end=publish_end,
                include_netlocs=include_netlocs,
                exclude_netlocs=exclude_netlocs,
                visited_start=visited_start,
                visited_end=visited_end,
                certain=certain,
                include_companies=include_companies,
                exclude_companies=exclude_companies,
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
            return result.to_dict()

    except Exception as e:
        return {"error": str(e)}


@mcp.tool(name="scrape-url")
def scrape_url(
    html: str = "",
    recrawl: bool = False,
    render: bool = False,
    url: str = None
) -> dict:
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
    A dict containing: (e.g. data.full_text returns the full text of the topic).

    full_text : str
        The full textual content of the web page, or None if not available
    languages : dict
        A dictionary mapping language codes to their probabilities or counts, representing detected languages.
    metadata : dict
        Metadata extracted from the web page, such as description, keywords, author, etc.
    page : dict
        Page-specific details, such as title, canonical URL, and other page-level information.
    request : dict
        Information about the HTTP request and response, such as headers, status code, and timing.
    snippets : SnippetSet
        A set of extracted text snippets or highlights from the page, wrapped in a SnippetSet object.
    statistics: dict
        Statistical information about the page, such as word count, sentence count, or other computed metrics.
    structured : list
        A list of structured data objects (e.g., schema.org, OpenGraph) extracted from the page.
    url_tree: dict
        A hierarchical representation of the URL structure, such as breadcrumbs or navigation paths.
    companies : list
        A list of companies extracted from the page.
    """
    # Lazy import keeps server startup instant
    from nosible import Nosible

    key = _get_key()
    try:
        # Prefer constructor param so we don't touch process-wide env
        with Nosible(nosible_api_key=key) as nos:
            result = nos.scrape_url(
                html=html,
                recrawl=recrawl,
                render=render,
                url=url,
            )
            return result.to_dict()

    except Exception as e:
        return {"error": str(e)}


@mcp.tool(name="topic-trend")
def topic_trend(
    query: str,
    start_date: str = None,
    end_date: str = None,
) -> dict:
    """
    Extract a topic's trend showing the volume of news surrounding your query.

    Parameters
    ----------
    query : str
        The search term we would like to see a trend for.
    start_date : str
        ISO‐format start date (YYYY-MM-DD) of the trend window.
    end_date : str
        ISO‐format end date (YYYY-MM-DD) of the trend window.

    Returns
    -------
    The JSON-decoded topic trend data returned by the server.

    e.g. {'2005-01-31': ...'2020-12-31': ...}
    """
    # Lazy import keeps server startup instant
    from nosible import Nosible

    key = _get_key()
    try:
        # Prefer constructor param so we don't touch process-wide env
        with Nosible(nosible_api_key=key) as nos:
            result = nos.topic_trend(
                query=query,
                start_date=start_date,
                end_date=end_date,
            )
            return result

    except Exception as e:
        return {"error": str(e)}