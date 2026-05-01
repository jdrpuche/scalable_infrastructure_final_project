from langchain_core.tools import tool
from firebase.clients import list_clients, get_client
from tools.tavily_search import tavily_search


@tool
async def search_web(query: str) -> str:
    """Search the web for up-to-date information using Tavily."""
    try:
        results = await tavily_search(query)
    except Exception as e:
        return f"Web search unavailable: {e}"
    if not results:
        return "No results found."
    return "\n\n".join(
        f"**{r['title']}**\n{r['url']}\n{r.get('content', '')}" for r in results
    )


@tool
async def get_all_clients(_: str = "") -> str:
    """Return a list of all clients stored in the database."""
    clients = await list_clients()
    if not clients:
        return "No clients found."
    return "\n".join(f"- ID: {c['id']} | {c['name']} ({c['email']})" for c in clients)


@tool
async def get_client_info(client_id: str) -> str:
    """Get detailed information about a specific client by their ID."""
    client = await get_client(client_id)
    if not client:
        return f"Client with id '{client_id}' not found."

    prefs = client.get("preferences") or {}
    brands = ", ".join(prefs.get("brands", [])) or "N/A"
    types = ", ".join(prefs.get("types", [])) or "N/A"

    history = client.get("history") or []
    history_lines = "\n".join(
        f"  - {h['product']} (viewed: {h['viewed_at']})" for h in history
    ) or "  N/A"

    purchases = client.get("purchases") or []
    purchase_lines = "\n".join(
        f"  - {p['product']} x{p['quantity']} — {p['price']}€ ({p['purchased_at']})"
        for p in purchases
    ) or "  N/A"

    return (
        f"Name: {client['name']}\n"
        f"Email: {client['email']}\n"
        f"Phone: {client.get('phone', 'N/A')}\n"
        f"Notes: {client.get('notes', 'N/A')}\n"
        f"Preferred brands: {brands}\n"
        f"Preferred guitar types: {types}\n"
        f"Viewed products:\n{history_lines}\n"
        f"Purchases:\n{purchase_lines}"
    )


tools = [search_web, get_all_clients, get_client_info]
