from fastapi import APIRouter, HTTPException
from schemas import ClientProfile
from firebase.clients import create_client, get_client, list_clients, update_client, delete_client

router = APIRouter()


@router.get("/")
async def index():
    return await list_clients()


@router.post("/")
async def create(body: ClientProfile):
    doc_id = await create_client(body.model_dump(exclude={"id"}))
    return {"id": doc_id}


@router.get("/{client_id}")
async def read(client_id: str):
    client = await get_client(client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@router.put("/{client_id}")
async def update(client_id: str, body: ClientProfile):
    ok = await update_client(client_id, body.model_dump(exclude={"id"}, exclude_none=True))
    if not ok:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"updated": True}


@router.delete("/{client_id}")
async def delete(client_id: str):
    ok = await delete_client(client_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"deleted": True}
