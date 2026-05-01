from datetime import datetime, timezone
from firebase.client import get_db


COLLECTION = "chat_history"


def _session_ref(session_id: str):
    return get_db().collection(COLLECTION).document(session_id)


async def append_message(session_id: str, role: str, content: str) -> None:
    ref = _session_ref(session_id)
    doc = ref.get()
    messages = doc.to_dict().get("messages", []) if doc.exists else []
    messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    ref.set({"messages": messages}, merge=True)


async def get_history(session_id: str) -> list[dict]:
    doc = _session_ref(session_id).get()
    if not doc.exists:
        return []
    return doc.to_dict().get("messages", [])


async def clear_history(session_id: str) -> None:
    _session_ref(session_id).delete()
