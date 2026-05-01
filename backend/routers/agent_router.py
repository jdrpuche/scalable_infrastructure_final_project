from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from schemas import ChatMessage
from agent.agent import run_agent, stream_agent
from firebase.chat_history import get_history

router = APIRouter()


@router.post("/chat")
async def chat(body: ChatMessage):
    response = await run_agent(body.session_id, body.user_id, body.message)
    return {"response": response}


@router.post("/stream")
async def stream(body: ChatMessage):
    async def generator():
        async for chunk in stream_agent(body.session_id, body.user_id, body.message):
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generator(), media_type="text/event-stream")


@router.get("/history/{session_id}")
async def history(session_id: str):
    messages = await get_history(session_id)
    return {"messages": messages}
