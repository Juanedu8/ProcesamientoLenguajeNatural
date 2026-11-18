"""Clase 11 - Starter del estudiante (NO la solucion).

Implementa aqui los TODOs T2-T6 siguiendo SPEC.md, PLAN.md y los skills en
../skills/. La referencia del profesor esta en ../solucion-referencia/app/
y NO se puede copiar: la nota esta en tu demo en vivo + check.py en verde.
"""
import os

import streamlit as st

DEFAULT_CHAT = "http://localhost:5678/webhook/agente-logistica-unal"
DEFAULT_INGEST = "http://localhost:5678/webhook/ingesta-reporte-pdf"

st.set_page_config(page_title="UNAL Logistica - Agente", layout="wide")
st.title("Agente de logistica UNAL — Interfaz Clase 11")

with st.sidebar:
    st.header("Conexion")
    chat_url = st.text_input("N8N_CHAT_URL", os.getenv("N8N_CHAT_URL", DEFAULT_CHAT))
    ingest_url = st.text_input("N8N_INGEST_URL", os.getenv("N8N_INGEST_URL", DEFAULT_INGEST))
    session_id = st.text_input("session_id (memoria)", "demo-01")
    st.caption("Mismo session_id = misma conversacion (Window Buffer Memory).")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_summary" not in st.session_state:
    st.session_state.last_summary = ""


# TODO(T2): parsear [{"output": ...}] o {"output": ...} a str.
def parse_output(data):
    raise NotImplementedError("T2: implementa el parseo del contrato n8n")


# TODO(T2): POST {"sessionId","chatInput"} con timeout 120; 404/401 con mensaje
# en espanol segun skills/n8n-webhook-client/SKILL.md.
def post_chat(url, sid, msg):
    raise NotImplementedError("T2: implementa el cliente del Workflow A")


# TODO(T2): append user, chat_message, spinner, append assistant, render.
def send_and_render(prompt):
    raise NotImplementedError("T2: implementa el envio + render del chat")


tab_chat, tab_ground, tab_pdf, tab_report = st.tabs(
    ["Chat", "Inventario y clima", "Subir PDF", "Reporte"]
)

with tab_chat:
    # TODO(T2): historial con st.chat_message + st.chat_input -> send_and_render.
    st.info("TODO T2: historial y chat_input aqui.")

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
