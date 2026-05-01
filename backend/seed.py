"""
Populate Firestore with test clients from data/seed_clients.json.
Uses the client email as document ID so re-running overwrites instead of duplicating.
Usage: python seed.py
"""
import asyncio
import json
from pathlib import Path

from firebase.clients import create_client


async def main():
    path = Path(__file__).parent / "data" / "seed_clients.json"
    clients = json.loads(path.read_text())
    for client in clients:
        doc_id = await create_client(client, doc_id=client["email"])
        print(f"Upserted client: {doc_id} — {client['name']}")


if __name__ == "__main__":
    asyncio.run(main())
