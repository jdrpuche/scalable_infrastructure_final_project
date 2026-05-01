from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.agent_router import router as agent_router
from routers.clients_router import router as clients_router
from routers.tools_router import router as tools_router

app = FastAPI(title="Mi Asistente API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agent_router, prefix="/agent", tags=["agent"])
app.include_router(clients_router, prefix="/clients", tags=["clients"])
app.include_router(tools_router, prefix="/tools", tags=["tools"])


@app.get("/health")
async def health():
    return {"status": "ok"}
