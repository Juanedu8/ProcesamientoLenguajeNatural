# Skill: pdf-report

Úsala para subida y generación de PDF en `app/app.py`.

## Subir (ingesta)
- `st.file_uploader("PDF", type=["pdf"])`, rechazar > 10 MB con `st.error`.
- Extraer con `pypdf`: `PdfReader(file).pages → extract_text()`, unir con `\n`,
  truncar a 20000 chars. Si queda vacío (escaneado), avisar y no enviar.
- Preview de 1000 chars en `st.expander`, luego POST al Workflow B
  (ver skill n8n-webhook-client) y render de `summary`.

## Generar (reporte)
- Con `fpdf2`: portada (título, sesión, fecha), sección por intercambio
  (`user:` / `agente:` con `multi_cell`), cierre con último `summary` si existe.
- Fuente base `Helvetica`, `latin-1` con reemplazo (`á→a` no: usar
  `.encode("latin-1", "replace")`) o `DejaVu` si está disponible.
- Entregar con `st.download_button("Descargar reporte.pdf", bytes, "reporte.pdf")`.
- Dependencias: `pypdf, fpdf2`. Probar con `poema_test.pdf` y `reporte_planta.pdf`.
