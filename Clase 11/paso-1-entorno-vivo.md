# Paso 1 — T0: entorno vivo (para hacer ANTES de codificar)

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

## 3. Importa los DOS workflows y publícalos

1. Abre n8n por la URL `https` de la pestaña `PORTS` (puerto 5678),
   **nunca** por `http://localhost:5678` en el navegador.
2. `Workflows → … → Import from file`, uno por uno:
   - `Clase 10/Clase10 - Agente Logistica UNAL.json`
   - `Clase 11/n8n-workflow-ingesta-pdf.json`
3. En cada uno pulsa **`Publish`** arriba a la derecha (eso es el `Active`).
4. Copia sus Production URLs del nodo Webhook:
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

## 6. Checkpoint (avísame esto para pasar al paso 2)
1. `docker compose ps` → n8n `Up`.
2. `Status: 200` del punto 4 (pega las 2 primeras líneas).
3. Conteo del check (`3/9`, `4/9`...).
