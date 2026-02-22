from duckduckgo_search import DDGS

def web_search(query: str, max_results: int = 5):
    """
    Performs a web search using DuckDuckGo and returns the results.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
        return results if results else []
