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

## Paso 2 — T2 con OpenCode: el orquestador trabaja, tú diriges

> Meta: `check.py` enciende `cliente chat` + `chat UI` (5/9) SIN que tú escribas
> el código: lo implementan tus subagentes y tú verificas. Sentido del paso:
> practicar SDD — el SPEC manda, el orquestador delega, los skills dan contexto,
> TASKS + `check.py` son el juez. Trabajan SOLO en `Clase 11/starter/app.py`.
> La referencia (`solucion-referencia/`) no se mira ni se menciona.

## 6. Abre OpenCode y lánzale el T2 (copia y pega este prompt)

```bash
cd /workspaces/ProcesamientoLenguajeNatural
opencode
```

Pega esto como primer mensaje (es tu contrato con el orquestador):
```text
Rol: orquestador de la Clase 11. Ejecuta SOLO la tarea T2 de TASKS.md.
Lee antes: Clase 11/SPEC.md (historias chat+memoria y criterios), Clase 11/PLAN.md
(decision Streamlit), Clase 11/TASKS.md (T2), Clase 11/AGENTS.md (las 7 reglas)
y los skills Clase 11/skills/n8n-webhook-client/SKILL.md +
Clase 11/skills/streamlit-chat-ui/SKILL.md.
Delega: explore verifica el contrato vivo con Peticion.py (Status 200);
frontend implementa UNICAMENTE T2 en Clase 11/starter/app.py
(parse_output, post_chat con timeout 120 y errores 404/401 en espanol,
send_and_render, pestana Chat con historial + chat_input).
Prohibido: tocar solucion-referencia/, commitear secretos, salirte de starter/,
implementar T3-T6. Hecho = check.py con cliente chat + chat UI en PASS.
Evidencia: comando + output pegados en tu resumen.
```

Reglas de lanzamiento que aprendimos a golpes:
- **Un T por lanzamiento**: si le pides T2–T6 de una, mezcla todo y el juez no te dice qué falló.
- **Pega el prompt completo**: sin los archivos de contexto el agente inventa el contrato (otro puerto, otro payload).
- **Trabaja en foreground**: mira lo que hace en vivo, no lo dejes solo hasta el T4.

✅ Esperado: el orquestador responde con su plan (explore → frontend) y empieza a trabajar. Si en cambio te pregunta qué hacer, no pegaste el contexto: repite el prompt.

## 7. Supervisa a los subagentes (tú eres el QA, no el teclista)

- `explore` debe mostrarte `Status: 200` de `Peticion.py`. Si no lo logra, el problema es n8n (vuelve al punto 4 del paso 1), no el código: detén al orquestador y arregla n8n tú.
- `frontend` solo puede tocar `starter/app.py`. Vigila con:
```bash
git status --short; git diff --stat
```
- ❌ Si ves cambios fuera de `starter/` (referencia, workflows, Pagina): detén y redirige con la regla 1 de `AGENTS.md`: *"SPEC manda: solo T2 en starter/app.py, revierte el resto"*.
- ❌ Si propone credenciales quemadas o URLs distintas a las del SPEC: detén y redirige con la regla 2: *"nada de secretos en el repo, URLs solo de variables + sidebar"*.

## 8. Verifica TÚ (el juez no se delega)

```bash
python "Clase 11/starter/check.py"
streamlit run "Clase 11/starter/app.py"   # UI en :8501 de PORTS
```

✅ Esperado en el juez: `cliente chat` + `chat UI` en `PASS` → 5/9 en verde.

En la UI, con `session_id demo-01`:
1. Pregunta "¿Hay osciloscopios?" → responde el agente.
2. Pregunta "¿y dónde están?" (mismo session) → usa contexto (memoria OK).
3. Cambia a `demo-02`, repite → empieza de cero (memoria aislada OK).

- ❌ Si el spinner nunca termina: n8n caído o workflow sin `Publish`. Vuelve al punto 4 del paso 1.
- ❌ Si el juez sigue en FAIL tras el agente: pégale al orquestador el output tal cual de `check.py` y pídele que corrija solo eso.

Si todo está en verde, cierra el T2 como se debe:
```bash
git add "Clase 11/starter/app.py"; git commit -m "T2: chat + memoria via orquestador (check 5/9)"
```

## Checkpoint del paso 2 (avísame esto para agregar aquí el paso 3)
1. `check.py` en 5/9 (pega el conteo).
2. `git log --oneline -1` de tu commit T2.
3. Qué respondió a "¿y dónde están?" con `demo-01`.
