from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    session_id: str
    user_id: str
    message: str


class GuitarPreferences(BaseModel):
    brands: list[str] = []
    types: list[str] = []


class ViewedProduct(BaseModel):
    product: str
    viewed_at: str


class Purchase(BaseModel):
    product: str
    price: float
    quantity: int
    purchased_at: str


class ClientProfile(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    phone: Optional[str] = None
    notes: Optional[str] = None
    preferences: Optional[GuitarPreferences] = None
    history: Optional[list[ViewedProduct]] = None
    purchases: Optional[list[Purchase]] = None


class ToolSearchRequest(BaseModel):
    query: str
    max_results: int = 5
