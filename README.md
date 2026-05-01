# Mi Asistente

Asistente conversacional con agente LangChain, FastAPI, Firebase Firestore y React.

## Estructura

```
mi-asistente/
├── backend/          # FastAPI + LangChain agent
└── frontend/         # React + Vite
```

## Backend

### Requisitos
- Python 3.11+
- Credenciales de Firebase (`firebase-service-account.json`)
- Claves de API en `backend/.env`

### Configuración

```bash
cd backend
cp .env.example .env   # completa las claves
pip install -r requirements.txt
```

### Variables de entorno (`backend/.env`)

```
OPENAI_API_KEY=sk-...
TAVILY_API_KEY=tvly-...
FIREBASE_CREDENTIALS_PATH=firebase-service-account.json
```

### Iniciar servidor

```bash
uvicorn main:app --reload
```

### Seed de clientes de prueba

```bash
python seed.py
```

## Frontend

### Requisitos
- Node 18+

### Instalar y ejecutar

```bash
cd frontend
npm install
npm run dev
```

La app estará disponible en `http://localhost:5173`.

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/agent/chat` | Chat con el agente |
| POST | `/agent/stream` | Chat en streaming (SSE) |
| GET | `/clients/` | Listar clientes |
| POST | `/clients/` | Crear cliente |
| GET | `/clients/{id}` | Obtener cliente |
| PUT | `/clients/{id}` | Actualizar cliente |
| DELETE | `/clients/{id}` | Eliminar cliente |
| POST | `/tools/search` | Búsqueda web con Tavily |
