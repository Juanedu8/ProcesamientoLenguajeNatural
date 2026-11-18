# TASKS — Clase 11 (orquestador: tomar en orden, una a la vez)

- [ ] **T1 Contrato vivo.** Verificar `docker compose ps` (n8n Up), workflow A en
      `Publish`, `POST localhost:5678/webhook/agente-logistica-unal` con
      `Peticion.py` responde `output`. Evidencia: comando + `Status: 200`.
- [ ] **T2 Chat + memoria.** `app/app.py`: sidebar (`N8N_CHAT_URL`, `session_id`),
      historial en `st.session_state`, parseo `[{output}]/{output}`, timeout 120 s,
      estados vacío/error. Evidencia: `py_compile` + captura de 2 turnos mismo `sessionId`.
- [ ] **T3 Panel grounding.** Botones `Osciloscopios / Raspberry Pi / Clima Manizales`
      que envían el `chatInput` correspondiente y muestran respuesta + JSON crudo
      colapsable. Evidencia: 3 respuestas reales.
- [ ] **T4 Escritura con confirmación.** Formulario `ID/Componente/Cantidad/Ubicacion/Estado`
      + checkbox `Confirmo` + preview del `chatInput` generado
      (`Registra: ID=... Componente=...`). Sin check no hay POST. Documentar alta del
      tool `Inventario_Write` en n8n. Evidencia: ejecución que devuelve confirmación.
- [ ] **T5 Subir PDF.** `file_uploader` PDF ≤10 MB, extracción con `pypdf`, preview
      1000 chars, `POST {N8N_INGEST_URL}` con `{"sessionId","filename","text"}`,
      render de `summary`. Probar con `poema_test.pdf` y `reporte_planta.pdf`.
- [ ] **T6 Generar reporte.** Botón que arma PDF con `fpdf2` (sesión, fecha, intercambios,
      último resumen) y `download_button`. Evidencia: PDF descargado con ≥1 intercambio.
- [ ] **T7 Workflow B.** Importar `n8n-workflow-ingesta-pdf.json`, `Publish`, probar con
      `curl` JSON `{"sessionId","filename","text"}` → `{"ok":true,"summary":...}`.
- [ ] **T8 QA + vitrina.** `grep` de secretos vacío, `py_compile` ok, probar T2–T6 contra
      n8n real, actualizar `Pagina/unidad-3/clase-11.html` (qué hace, arquitectura,
      cómo correr Streamlit, link al SPEC). Evidencia: checklist SPEC §4 en verde.

Reparto sugerido: orquestador → `explore` (T1), `frontend` (T2–T6), `qa` (T7–T8).
Cada tarea cierra con comando + output pegado en el resumen.
