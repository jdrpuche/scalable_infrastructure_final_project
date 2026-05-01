# Caso de Uso: Asistente Inteligente para E-Commerce de Guitarras

## Descripción General

Este sistema es un asistente conversacional basado en inteligencia artificial diseñado para apoyar a los agentes de venta de una tienda online de guitarras. Permite consultar el perfil completo de cada cliente —sus preferencias, historial de navegación y compras pasadas— y combinar esa información con búsquedas en tiempo real para ofrecer recomendaciones personalizadas y respuestas actualizadas.

---

## Actores

| Actor | Descripción |
|---|---|
| **Agente de ventas** | Usuario principal del sistema. Usa el chat para consultar información de clientes y productos. |
| **Cliente** | Persona registrada en la plataforma con historial de navegación y compras. |
| **Asistente IA** | Agente LLM (GPT-4o-mini) con acceso a herramientas de consulta y búsqueda web. |

---

## Flujo Principal

```
Agente de ventas
      │
      ▼
Selecciona un cliente en el desplegable
      │
      ▼
El sistema carga el historial de conversación previo (Firestore)
      │
      ▼
El agente escribe una consulta en el chat
      │
      ▼
El asistente IA decide qué herramientas usar:
  ├── get_all_clients()     → Lista todos los clientes con sus IDs
  ├── get_client_info()     → Perfil completo: preferencias, vistas y compras
  └── search_web()         → Búsqueda en tiempo real (precios, novedades, stock)
      │
      ▼
El asistente responde con información consolidada
      │
      ▼
La conversación queda guardada en Firestore (por sesión/cliente)
```

---

## Casos de Uso Específicos

### CU-01: Consultar el perfil de un cliente

**Actor:** Agente de ventas  
**Precondición:** El cliente existe en la base de datos.  
**Flujo:**
1. El agente selecciona al cliente en el desplegable.
2. Escribe: *"¿Qué marcas prefiere este cliente?"*
3. El asistente llama a `get_all_clients()` para obtener el ID, luego a `get_client_info()`.
4. Devuelve marcas preferidas, tipos de guitarra y notas del perfil.

**Resultado esperado:** El agente conoce las preferencias del cliente antes de contactarle.

---

### CU-02: Revisar el historial de compras

**Actor:** Agente de ventas  
**Precondición:** El cliente tiene compras registradas.  
**Flujo:**
1. El agente pregunta: *"¿Cuál fue la última compra de María Fernández?"*
2. El asistente recupera el perfil completo del cliente.
3. Muestra la lista de compras con producto, cantidad, precio y fecha.

**Resultado esperado:** El agente puede hacer un seguimiento postventa o sugerir accesorios complementarios.

---

### CU-03: Consultar disponibilidad o precio en tiempo real

**Actor:** Agente de ventas  
**Precondición:** El asistente tiene acceso a Tavily Search.  
**Flujo:**
1. El agente pregunta: *"¿Cuál es el precio actual de la Fender Stratocaster American Professional II?"*
2. El asistente detecta que necesita información actualizada y llama a `search_web()`.
3. Devuelve resultados de tiendas online con precio, disponibilidad y enlace.

**Resultado esperado:** El agente puede dar al cliente información de precios actualizada sin salir del chat.

---

### CU-04: Recomendar productos basados en preferencias

**Actor:** Agente de ventas  
**Flujo:**
1. El agente pregunta: *"¿Qué guitarra le recomendarías a Carlos López?"*
2. El asistente combina el perfil del cliente (Yamaha, Taylor, acústica/clásica, primer comprador) con una búsqueda web de modelos actuales.
3. Propone opciones adaptadas al nivel y presupuesto inferido del cliente.

**Resultado esperado:** Recomendación personalizada lista para comunicar al cliente.

---

### CU-05: Restaurar el historial de conversación

**Actor:** Agente de ventas  
**Precondición:** El agente ya tuvo una conversación previa con el contexto de ese cliente.  
**Flujo:**
1. El agente cierra y vuelve a abrir el navegador.
2. Selecciona al mismo cliente en el desplegable.
3. El sistema carga automáticamente el historial de mensajes desde Firestore.

**Resultado esperado:** La conversación continúa donde se dejó, sin perder contexto.

---

## Arquitectura del Sistema

```
┌─────────────────────────────────┐
│         Frontend (React)        │
│  - Selector de cliente          │
│  - Chat con historial           │
│  - Vite dev server (:5173)      │
└────────────┬────────────────────┘
             │ HTTP (proxy /api)
┌────────────▼────────────────────┐
│        Backend (FastAPI)        │
│  - /agent/chat   POST           │
│  - /agent/history/{id}  GET     │
│  - /clients/     GET            │
└──────┬──────────────┬───────────┘
       │              │
┌──────▼──────┐ ┌─────▼──────────┐
│  LangGraph  │ │    Firestore   │
│  + GPT-4o   │ │  · clients     │
│  + Tavily   │ │  · chat_history│
└─────────────┘ └────────────────┘
```

---

## Datos del Cliente

Cada cliente almacenado en Firestore contiene:

```json
{
  "name": "Ana García",
  "email": "ana.garcia@example.com",
  "phone": "+34 600 111 222",
  "notes": "Cliente preferente. Interesada en guitarras eléctricas de gama alta.",
  "preferences": {
    "brands": ["Fender", "Gibson"],
    "types": ["Eléctrica", "Semi-hollow"]
  },
  "history": [
    { "product": "Fender Stratocaster American Professional II", "viewed_at": "2026-04-10T10:30:00Z" }
  ],
  "purchases": [
    { "product": "Fender Stratocaster American Professional II", "price": 1499.99, "quantity": 1, "purchased_at": "2026-04-15T11:00:00Z" }
  ]
}
```

---

## Tecnologías Utilizadas

| Capa | Tecnología |
|---|---|
| Frontend | React 18, Vite 5 |
| Backend | FastAPI, Python 3.11+ |
| Agente IA | LangGraph, LangChain, GPT-4o-mini |
| Búsqueda web | Tavily Search API |
| Base de datos | Firebase Firestore |
| Despliegue local | WSL2 + uvicorn |
