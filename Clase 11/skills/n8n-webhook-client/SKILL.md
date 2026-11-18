# Skill: n8n-webhook-client

Úsala cuando llames a los webhooks de las Clases 10/11.

## Contrato chat (Workflow A)
- `POST {N8N_CHAT_URL}` header `Content-Type: application/json`, timeout 120.
- Body: `{"sessionId": "<estable>", "chatInput": "<texto>"}`.
- Respuesta: `[{"output": "..."}]` o `{"output": "..."}`. Función de parseo:
  si es lista, tomar `[0]["output"]`; si es dict, `["output"]`; si no, mostrar JSON crudo.
- `404` → workflow no publicado o path con `/webhook-test/` en vez de `/webhook/`.
- `401` vacío → URL `https://...app.github.dev` con puerto `Private`: usar
  `http://localhost:5678/...` dentro del Codespace o pasar el puerto a `Public`.

## Contrato ingesta (Workflow B)
- `POST {N8N_INGEST_URL}` con `{"sessionId","filename","text"}` (`text` ≤ 20000 chars).
- Respuesta: `{"ok": true, "filename": "...", "summary": "...", "chars": N}`.

## Ejemplo
```python
import requests
r = requests.post(url, json={"sessionId": sid, "chatInput": msg}, timeout=120)
r.raise_for_status()
data = r.json()
out = data[0]["output"] if isinstance(data, list) else data.get("output", data)
```
