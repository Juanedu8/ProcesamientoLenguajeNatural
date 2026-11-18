# Starter — Clase 11 (rol estudiante)

Eres el estudiante. La referencia del profesor (`../solucion-referencia/app/`)
existe pero **mirarla es perder el ejercicio**: la nota esta en tu demo en vivo.

## Flujo (igual que manana en tu Codespace)

```bash
cd /workspaces/ProcesamientoLenguajeNatural/.devcontainer
docker compose up -d                                    # n8n en :5678
# en n8n: importar Clase 11/Clase11 - Agente Logistica UNAL.json -> Publish
# (2 ramas) y desactivar el workflow de la Clase 10 (mismo path de chat)
# en n8n: verificar Clase10 - Agente Logistica UNAL en Publish
pip install -r "Clase 11/starter/requirements.txt"
python "Clase 11/starter/check.py"                      # juez: debe subir 0/9 -> 9/9
streamlit run "Clase 11/starter/app.py"                 # UI en :8501
```

## Reglas
1. Implementa los TODOs `T2..T6` en `app.py` en orden (`TASKS.md`).
2. Cada TODO cerrado se verifica con `python "Clase 11/starter/check.py"`.
3. `check.py` en verde NO basta: prepara la demo (chat con memoria, escritura
   con y sin check, ingesta de `poema_test.pdf`, reporte descargado) porque la
   nota es la demo + 3 preguntas de decisiones (por que Streamlit, por que B
   separado, por que doble confirmacion).
