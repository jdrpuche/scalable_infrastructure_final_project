from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import create_react_agent

from config import settings
from agent.tools_langchain import tools
from firebase.chat_history import get_history, append_message

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=settings.openai_api_key,
    temperature=0.3,
)

graph = create_react_agent(llm, tools=tools)


def _to_lc_messages(history: list[dict]):
    result = []
    for msg in history:
        if msg["role"] == "user":
            result.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            result.append(AIMessage(content=msg["content"]))
    return result


async def run_agent(session_id: str, user_id: str, message: str) -> str:
    history = await get_history(session_id)
    messages = _to_lc_messages(history) + [HumanMessage(content=message)]

    result = await graph.ainvoke({"messages": messages})
    ai_message = result["messages"][-1]
    response_text = ai_message.content

    await append_message(session_id, "user", message)
    await append_message(session_id, "assistant", response_text)

    return response_text


async def stream_agent(session_id: str, user_id: str, message: str):
    history = await get_history(session_id)
    messages = _to_lc_messages(history) + [HumanMessage(content=message)]

    full_response = []
    async for chunk in graph.astream({"messages": messages}):
        if "agent" in chunk:
            for msg in chunk["agent"]["messages"]:
                if hasattr(msg, "content") and msg.content:
                    full_response.append(msg.content)
                    yield msg.content

    await append_message(session_id, "user", message)
    await append_message(session_id, "assistant", "".join(full_response))
