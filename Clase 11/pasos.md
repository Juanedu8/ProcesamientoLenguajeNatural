# Pasos — Clase 11 (rol estudiante)

Guía operativa paso a paso. Cada paso termina con un checkpoint: no avances al
siguiente sin tenerlo en verde. Los pasos 2, 3, ... se van concatenando aquí.

## Paso 1 — T0: entorno vivo (para hacer ANTES de codificar)

> Meta del paso: n8n `Up`, 2 workflows en `Publish`, contrato verificado con
> `Status: 200` y `check.py` en **3/9 en verde**. Sin esto, nada de T2.

## 1. Fork y Codespace (rol estudiante)

1. En GitHub: `Fork` del repo (si no lo tienes) → en TU fork
   `Code > Codespaces > Create codespace on main`.
2. Todo lo de abajo se hace **dentro del Codespace**, no en tu Windows.
   El n8n y el Streamlit solo existen ahí.

## 2. Actualiza y levanta SOLO el n8n (no el compose completo)

```bash
git pull
cd /workspaces/ProcesamientoLenguajeNatural/.devcontainer
docker pull n8nio/n8n:latest
docker compose up -d n8n
docker compose ps
docker compose logs --tail=20 n8n
```

Reglas que aprendimos a golpes:
- **NUNCA `docker compose up -d` completo**: el compose incluye el servicio
  `dev`, que es el contenedor donde estás parado. Recrearlo mata tu sesión
  y ves "the codespace is not available".
- **`pull` separado primero**: la imagen pesa cientos de MB; así ves el
  progreso en vez de una terminal congelada.
- **No mezcles descargas**: espera a que termine el "Setting up" del
  `postCreateCommand` antes del `docker pull` (2 cores no dan para todo a la vez).

✅ Esperado: `pln-clase10-n8n-n8n-1 Up ... 0.0.0.0:5678->5678/tcp` y en los
logs `Editor is ready` / `n8n ready on ::, port 5678`.

### Si el Codespace muere ("not available")
1. En otra pestaña abre `github.com/codespaces` y mira el estado:
   - `Running` → espera 3–5 min (estaba descargando) y reabre.
   - `Failed` → `Restart`; si no revive, `Delete` + `Create codespace on main`.
2. No pierdes nada: todo está en git. Solo reimportarías los workflows (punto 3).

## 3. Importa el workflow único (2 ramas) y publícalo

1. Abre n8n por la URL `https` de la pestaña `PORTS` (puerto 5678),
   **nunca** por `http://localhost:5678` en el navegador.
2. `Workflows → … → Import from file`:
   - `Clase 11/Clase11 - Agente Logistica UNAL.json` (rama chat + rama ingesta)
3. Pulsa **`Publish`** arriba a la derecha (eso es el `Active`) y **desactiva
   el workflow de la Clase 10** si lo tienes: comparten el `path`
   `agente-logistica-unal` y dos activos = doble disparo.
4. Copia sus Production URLs de los nodos Webhook:
   - `.../webhook/agente-logistica-unal`
   - `.../webhook/ingesta-reporte-pdf`

## 4. Verifica el contrato (Clase 10 manda)

```bash
cd /workspaces/ProcesamientoLenguajeNatural
python "Clase 10/Peticion.py" --url http://localhost:5678/webhook/agente-logistica-unal --mensaje "¿Hay osciloscopios?" --session-id paso01
```

- ✅ `Status: 200` + respuesta del agente → sigue al punto 5.
- ❌ `404` → el workflow no está publicado o usas `/webhook-test/`. Publica y usa `/webhook/`.
- ❌ `401` con body vacío → usaste la URL `https://...app.github.dev` con el
  puerto en `Private` desde dentro del Codespace. Repite con
  `http://localhost:5678/...` tal cual.

## 5. Starter + juez

```bash
pip install -r "Clase 11/starter/requirements.txt"
python "Clase 11/starter/check.py"
```

✅ Esperado:
```
[PASS] py_compile app.py
[PASS] sin secretos en app.py
[FAIL] cliente chat ...
[FAIL] chat UI ...
[FAIL] grounding ...
[FAIL] escritura ...
[FAIL] PDF ...
[PASS] requirements ...
[SKIP/PASS] contrato vivo
3/9 en verde (4/9 si n8n responde).
```

## Checkpoint del paso 1 (listo si tienes esto)
1. `docker compose ps` → n8n `Up`.
2. `Status: 200` del punto 4.
3. `check.py` en 3/9 (4/9 si n8n respondió al contrato vivo).

## Paso 2 — T2: chat + memoria (primer código del starter)

> Meta: `check.py` enciende `cliente chat` + `chat UI` (5/9) y el Streamlit
> conversa con memoria real. Trabaja SOLO en `Clase 11/starter/app.py`.
> La referencia (`solucion-referencia/`) no se mira.

### 1. `parse_output(data)` — el contrato de la 10 en una función
```python
def parse_output(data):
    if isinstance(data, list) and data and isinstance(data[0], dict) and "output" in data[0]:
        return str(data[0]["output"])
    if isinstance(data, dict) and "output" in data:
        return str(data["output"])
    return None  # el llamador muestra el JSON crudo
```

### 2. `post_chat(url, sid, msg)` — skill `n8n-webhook-client`
```python
r = requests.post(url, json={"sessionId": sid, "chatInput": msg}, timeout=120)
```
- `404` → `raise RuntimeError("404: workflow no publicado o path mal (usa /webhook/, no /webhook-test/).")`
- `401` → `raise RuntimeError("401: puerto 5678 en Private con URL https. Usa http://localhost:5678/... o pon el puerto en Public.")`
- `r.raise_for_status()`, luego `r.json()` en `try/except ValueError` (si no es JSON, devuelve `r.text`).
- Retorna `parse_output(data)` si no es `None`, si no el texto crudo.

### 3. `send_and_render(prompt)` — el ciclo completo
1. `st.session_state.messages.append({"role": "user", "content": prompt})`
2. `with st.chat_message("user"): st.markdown(prompt)`
3. `with st.chat_message("assistant"), st.spinner("Consultando al agente..."):`
   `try: answer = post_chat(...)` / `except Exception as e: answer = f"Error: {e}"`
4. Append del assistant + `st.markdown(answer)`. Retorna `answer` (lo reusa el T4).

### 4. Pestaña Chat — historial + entrada
```python
with tab_chat:
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
    if prompt := st.chat_input("Pregunta al agente (ej. ¿Hay osciloscopios?)"):
        send_and_render(prompt)
```

### 5. Verifica (juez + vivo)
```bash
python "Clase 11/starter/check.py"   # cliente chat + chat UI en PASS -> 5/9
streamlit run "Clase 11/starter/app.py"
```
En la UI (`:8501` en `PORTS`):
1. Pregunta "¿Hay osciloscopios?" con `session_id demo-01` → responde el agente.
2. Pregunta "¿y dónde están?" **mismo session** → usa contexto (memoria OK).
3. Cambia a `demo-02`, repite → empieza de cero (memoria aislada OK).

## Checkpoint del paso 2 (avísame esto para agregar aquí el paso 3)
1. `check.py` en 5/9 (pega el conteo).
2. Las 3 pruebas de memoria de la UI (qué respondió a "¿y dónde están?" con `demo-01`).
