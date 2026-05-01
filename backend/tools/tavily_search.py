import httpx
from config import settings

TAVILY_URL = "https://api.tavily.com/search"


async def tavily_search(query: str, max_results: int = 5) -> list[dict]:
    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(TAVILY_URL, json=payload)
        response.raise_for_status()
        data = response.json()
    return data.get("results", [])
