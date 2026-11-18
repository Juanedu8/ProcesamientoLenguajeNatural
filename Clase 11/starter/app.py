"""Clase 11 - Starter del estudiante (NO la solucion).

Implementa aqui los TODOs T2-T6 siguiendo SPEC.md, PLAN.md y los skills en
../skills/. La referencia del profesor esta en ../solucion-referencia/app/
y NO se puede copiar: la nota esta en tu demo en vivo + check.py en verde.
"""
import json
import os

import requests
import streamlit as st

DEFAULT_CHAT = "http://n8n:5678/webhook/agente-logistica-unal"
DEFAULT_INGEST = "http://n8n:5678/webhook/ingesta-reporte-pdf"

st.set_page_config(page_title="UNAL Logistica - Agente", layout="wide")
st.title("Agente de logistica UNAL — Interfaz Clase 11")

with st.sidebar:
    st.header("Conexion")
    chat_url = st.text_input("N8N_CHAT_URL", os.getenv("N8N_CHAT_URL", DEFAULT_CHAT))
    ingest_url = st.text_input("N8N_INGEST_URL", os.getenv("N8N_INGEST_URL", DEFAULT_INGEST))
    session_id = st.text_input("session_id (memoria)", "demo-01")
    st.caption("Mismo session_id = misma conversacion (Window Buffer Memory).")
    st.caption(
        "Memoria (Window Buffer Memory): si cambias el session_id arriba empiezas una "
        "conversación nueva; si lo mantienes igual, el agente recuerda los turnos anteriores."
    )
    for _url in (chat_url, ingest_url):
        if _url and ("localhost" in _url or "webhook-test" in _url):
            st.warning(
                "Esa URL no funcionará desde el código: usa http://n8n:5678/... para el "
                "webhook y /webhook/ (producción). localhost y /webhook-test/ solo sirven "
                "desde el navegador o con la UI de n8n en Execute workflow."
            )
            break

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""


# TODO(T2): parsear [{"output": ...}] o {"output": ...} a str.
def parse_output(data):
    """Extrae el texto del contrato de n8n; nunca lanza excepción."""
    claves = ("output", "text", "message", "response")
    try:
        if isinstance(data, list) and data and isinstance(data[0], dict):
            for clave in claves:
                if data[0].get(clave) is not None:
                    return str(data[0][clave])
        if isinstance(data, dict):
            for clave in claves:
                if data.get(clave) is not None:
                    return str(data[clave])
    except Exception:  # noqa: BLE001 - el parseo nunca debe romper la UI
        pass
    try:
        return json.dumps(data, ensure_ascii=False, indent=2)
    except Exception:  # noqa: BLE001
        return str(data)


# TODO(T2): POST {"sessionId","chatInput"} con timeout 120; 404/401 con mensaje
# en espanol segun skills/n8n-webhook-client/SKILL.md.
def post_chat(url, sid, msg):
    """Llama al Workflow A y devuelve el texto de la respuesta.

    Lanza RuntimeError con un mensaje en español y una pista accionable; la UI
    la captura en send_and_render para no exponer el traceback.
    """
    try:
        r = requests.post(url, json={"sessionId": sid, "chatInput": msg}, timeout=120)
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "No se pudo conectar a n8n. Verifica que el contenedor esté arriba con "
            "`docker compose up -d` y revisa `docker compose ps`."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Timeout de 120 s esperando a n8n. Confirma que el workflow esté en "
            "Publish/Active y vuelve a intentar."
        ) from exc
    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Error de red al llamar a n8n: {exc}") from exc

    if r.status_code == 404:
        raise RuntimeError(
            "404: workflow no publicado o path incorrecto. Publica el workflow en n8n "
            "y usa /webhook/ (no /webhook-test/). Verifica `docker compose ps`."
        )
    if r.status_code == 401:
        raise RuntimeError(
            "401: la URL no es accesible desde el código. Usa `http://n8n:5678/...` "
            "(localhost no llega al contenedor n8n); la URL https de PORTS es solo "
            "para el navegador."
        )
    if r.status_code >= 400:
        detalle = (r.text or "").strip()[:500]
        raise RuntimeError(
            f"{r.status_code}: n8n respondió con error. {detalle}".strip()
        )

    try:
        data = r.json()
    except ValueError:
        crudo = (r.text or "").strip()
        if not crudo:
            raise RuntimeError("n8n respondió 200 pero con cuerpo vacío.")
        return f"Respuesta no JSON de n8n (texto crudo):\n\n{crudo[:2000]}"

    return parse_output(data)


# TODO(T2): append user, chat_message, spinner, append assistant, render.
def send_and_render(prompt):
    """Agrega el turno del usuario, consulta a n8n y renderiza la respuesta."""
    prompt = (prompt or "").strip()
    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Consultando al agente..."):
        try:
            respuesta = post_chat(chat_url, session_id, prompt)
        except RuntimeError as exc:
            st.error(str(exc))
            return
        except Exception as exc:  # noqa: BLE001 - nunca mostrar traceback
            st.error(f"Error inesperado al consultar al agente: {exc}")
            return

    if not respuesta or not respuesta.strip():
        st.warning("El agente respondió vacío. Revisa el workflow en n8n o reformula la pregunta.")
        return

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
    with st.chat_message("assistant"):
        st.markdown(respuesta)


tab_chat, tab_ground, tab_pdf, tab_report = st.tabs(
    ["Chat", "Inventario y clima", "Subir PDF", "Reporte"]
)

with tab_chat:
    # TODO(T2): historial con st.chat_message + st.chat_input -> send_and_render.
    if not st.session_state.messages:
        st.info("Aún no hay mensajes. Pregunta, por ejemplo: ¿Hay osciloscopios?")
    else:
        for m in st.session_state.messages:
            with st.chat_message(m.get("role", "assistant")):
                st.markdown(m.get("content", ""))
        if st.button("Limpiar conversación"):
            st.session_state.messages = []
            st.rerun()

    prompt = st.chat_input("Escribe tu pregunta...")
    if prompt:
        send_and_render(prompt)

with tab_ground:
    # TODO(T3): 3 botones con chatInput fijo + expander JSON crudo.
    # TODO(T4): formulario ID/Componente/Cantidad/Ubicacion/Estado +
    #   checkbox "Confirmo" + preview. Sin check NO hay POST.
    st.info("TODO T3/T4: botones de grounding y formulario con confirmacion aqui.")

with tab_pdf:
    # TODO(T5): file_uploader PDF <=10 MB, extraer con pypdf (skills/pdf-report),
    #   preview 1000 chars, POST {"sessionId","filename","text"} al Workflow B.
    st.info("TODO T5: subida e ingesta de PDF aqui.")

with tab_report:
    # TODO(T6): armar PDF con fpdf2 (sesion, fecha, intercambios, ultimo summary)
    #   y download_button.
    st.info("TODO T6: generacion y descarga del reporte aqui.")
