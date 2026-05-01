from typing import Optional
from firebase.client import get_db


COLLECTION = "clients"


async def create_client(data: dict, doc_id: Optional[str] = None) -> str:
    db = get_db()
    ref = db.collection(COLLECTION).document(doc_id) if doc_id else db.collection(COLLECTION).document()
    ref.set(data)
    return ref.id


async def get_client(client_id: str) -> Optional[dict]:
    db = get_db()
    doc = db.collection(COLLECTION).document(client_id).get()
    if doc.exists:
        return {"id": doc.id, **doc.to_dict()}
    return None


async def list_clients() -> list[dict]:
    db = get_db()
    docs = db.collection(COLLECTION).stream()
    return [{"id": doc.id, **doc.to_dict()} for doc in docs]


async def update_client(client_id: str, data: dict) -> bool:
    db = get_db()
    ref = db.collection(COLLECTION).document(client_id)
    if not ref.get().exists:
        return False
    ref.update(data)
    return True


async def delete_client(client_id: str) -> bool:
    db = get_db()
    ref = db.collection(COLLECTION).document(client_id)
    if not ref.get().exists:
        return False
    ref.delete()
    return True
