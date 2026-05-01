import { useState, useEffect, useRef } from "react";
import { sendMessage, getClients, getHistory } from "./api";

export default function App() {
  const [clients, setClients] = useState([]);
  const [selectedClient, setSelectedClient] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    getClients().then(setClients).catch(console.error);
  }, []);

  useEffect(() => {
    if (!selectedClient) return;
    setMessages([]);
    getHistory(selectedClient.id)
      .then((history) =>
        setMessages(history.map((m) => ({ role: m.role, content: m.content })))
      )
      .catch(console.error);
  }, [selectedClient]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    if (!input.trim() || !selectedClient) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");
    setLoading(true);

    try {
      const data = await sendMessage(selectedClient.id, selectedClient.id, input);
      setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { role: "assistant", content: `Error: ${err.message}` }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 700, margin: "2rem auto", fontFamily: "sans-serif", padding: "0 16px" }}>
      <h1 style={{ marginBottom: 16 }}>Mi Asistente</h1>

      <select
        value={selectedClient?.id || ""}
        onChange={(e) => {
          const client = clients.find((c) => c.id === e.target.value) || null;
          setSelectedClient(client);
        }}
        style={{ width: "100%", padding: 10, marginBottom: 16, borderRadius: 6, border: "1px solid #ccc", fontSize: 14 }}
      >
        <option value="">— Selecciona un cliente —</option>
        {clients.map((c) => (
          <option key={c.id} value={c.id}>
            {c.name} ({c.email})
          </option>
        ))}
      </select>

      <div
        style={{
          border: "1px solid #ddd",
          borderRadius: 8,
          padding: 16,
          minHeight: 400,
          maxHeight: 500,
          marginBottom: 16,
          overflowY: "auto",
          background: selectedClient ? "#fff" : "#f9f9f9",
        }}
      >
        {!selectedClient && (
          <p style={{ color: "#aaa", textAlign: "center", marginTop: 80 }}>
            Selecciona un cliente para ver su historial de conversación.
          </p>
        )}

        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === "user" ? "right" : "left", marginBottom: 8 }}>
            <span
              style={{
                display: "inline-block",
                background: msg.role === "user" ? "#0070f3" : "#f0f0f0",
                color: msg.role === "user" ? "#fff" : "#000",
                padding: "8px 12px",
                borderRadius: 12,
                maxWidth: "75%",
                whiteSpace: "pre-wrap",
              }}
            >
              {msg.content}
            </span>
          </div>
        ))}

        {loading && <p style={{ color: "#888" }}>Pensando...</p>}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} style={{ display: "flex", gap: 8 }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={selectedClient ? "Escribe un mensaje..." : "Selecciona un cliente primero"}
          disabled={loading || !selectedClient}
          style={{ flex: 1, padding: 10, borderRadius: 6, border: "1px solid #ccc" }}
        />
        <button
          type="submit"
          disabled={loading || !selectedClient}
          style={{
            padding: "10px 20px",
            borderRadius: 6,
            background: selectedClient ? "#0070f3" : "#ccc",
            color: "#fff",
            border: "none",
            cursor: selectedClient ? "pointer" : "default",
          }}
        >
          Enviar
        </button>
      </form>
    </div>
  );
}
