from fastapi import APIRouter
from schemas import ToolSearchRequest
from tools.tavily_search import tavily_search

router = APIRouter()


@router.post("/search")
async def search(body: ToolSearchRequest):
    results = await tavily_search(body.query, body.max_results)
    return {"results": results}
