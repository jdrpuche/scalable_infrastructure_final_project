const BASE_URL = import.meta.env.VITE_API_URL || "/api";

export async function sendMessage(sessionId, userId, message) {
  const res = await fetch(`${BASE_URL}/agent/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, user_id: userId, message }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function streamMessage(sessionId, userId, message, onChunk) {
  const res = await fetch(`${BASE_URL}/agent/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: sessionId, user_id: userId, message }),
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const text = decoder.decode(value);
    const lines = text.split("\n").filter((l) => l.startsWith("data: "));
    for (const line of lines) {
      const chunk = line.replace("data: ", "");
      if (chunk !== "[DONE]") onChunk(chunk);
    }
  }
}

export async function getClients() {
  const res = await fetch(`${BASE_URL}/clients/`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

export async function getHistory(sessionId) {
  const res = await fetch(`${BASE_URL}/agent/history/${encodeURIComponent(sessionId)}`);
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return (await res.json()).messages;
}
