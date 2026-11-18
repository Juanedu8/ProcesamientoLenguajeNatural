# Skill: streamlit-chat-ui

Úsala para la UI de `Clase 11/app/app.py`.

- Sidebar: `N8N_CHAT_URL`, `N8N_INGEST_URL` (text_input con defaults localhost),
  `session_id` (text_input, default `demo-01`).
- Estado: `st.session_state.messages = [{"role": "user"/"assistant", "content": ...}]`.
- Chat: `st.chat_input` → `append user` → `requests.post` (skill n8n-webhook-client) →
  `append assistant` → `st.rerun` o render directo. Timeout 120 s, `try/except`
  con mensaje en español y pista (`Publica el workflow`, `docker compose ps`).
- Panel grounding: 3 botones que reutilizan la misma función de envío con
  `chatInput` fijo, más `st.expander("JSON crudo")`.
- Escritura: formulario + `checkbox Confirmo` + preview del texto generado.
  Sin check: `st.warning`, sin POST.
- Nunca hardcodear URLs ni keys en el código; solo `os.getenv` + sidebar.
