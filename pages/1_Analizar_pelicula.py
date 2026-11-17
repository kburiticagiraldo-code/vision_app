import base64
import json

import anthropic
import streamlit as st

from estilo import aplicar_estilo, hero
from mqtt_utils import publicar, veredicto

st.set_page_config(page_title="Analizar película", page_icon="🎞️", layout="centered")
aplicar_estilo()
hero("Analizar película", "Escribe el título o sube el póster y recibe la reseña del crítico.", "🎞️")

MODELO = "claude-sonnet-5-5"

SISTEMA = """Eres un crítico de cine exigente pero justo. Analiza la película indicada
(por título, por póster o por ambos). No inventes datos: si no reconoces la película,
pon "reconocida": false y explícalo en "resena".
Responde SOLO con un JSON válido, sin texto adicional ni bloques de código, así:
{
  "reconocida": true,
  "titulo": "...",
  "anio": "...",
  "director": "...",
  "genero": "...",
  "puntajes": {"guion": 0.0, "actuaciones": 0.0, "direccion": 0.0,
               "fotografia": 0.0, "banda_sonora": 0.0},
  "calificacion_final": 0.0,
  "puntos_fuertes": ["..."],
  "puntos_debiles": ["..."],
  "recomendada_para": "...",
  "resena": "Reseña de 120 a 180 palabras en español."
}
Todos los puntajes van de 0 a 10 con un decimal."""


def analizar(titulo, imagen):
    cliente = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    contenido = []
    if imagen is not None:
        contenido.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": imagen.type,
                    "data": base64.b64encode(imagen.getvalue()).decode(),
                },
            }
        )
    contenido.append({"type": "text", "text": f"Película: {titulo or '(identifícala por el póster)'}"})
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=1500,
        system=SISTEMA,
        messages=[{"role": "user", "content": contenido}],
    )
    texto = "".join(b.text for b in respuesta.content if b.type == "text")
    return json.loads(texto[texto.index("{") : texto.rindex("}") + 1])


titulo = st.text_input("🍿 Título de la película", placeholder="Ej: Parásitos")
imagen = st.file_uploader("🖼️ O sube el póster", type=["png", "jpg", "jpeg", "webp"])

if st.button("🎬 Analizar", type="primary", disabled=not (titulo or imagen)):
    with st.spinner("El crítico está viendo la película..."):
        try:
            st.session_state["analisis"] = analizar(titulo, imagen)
        except Exception as e:
            st.error(f"No se pudo analizar: {e}")

a = st.session_state.get("analisis")
if a:
    if not a.get("reconocida", True):
        st.warning(a.get("resena", "No reconocí la película."))
    else:
        nota = float(a["calificacion_final"])
        _, texto_v, emoji_v = veredicto(nota)

        st.markdown(f"## {a['titulo']} ({a['anio']})")
        st.caption(f"{a['director']} · {a['genero']}")
        c1, c2 = st.columns(2)
        c1.metric("Calificación final", f"{nota:.1f} / 10")
        c2.metric("Veredicto", f"{emoji_v} {texto_v}")

        st.markdown("### Puntajes")
        for nombre, valor in a["puntajes"].items():
            st.write(f"**{nombre.replace('_', ' ').capitalize()}**: {valor}")
            st.progress(min(max(float(valor) / 10, 0.0), 1.0))

        st.markdown("### Reseña")
        st.write(a["resena"])
        f, d = st.columns(2)
        with f:
            st.markdown("**👍 Puntos fuertes**")
            for p in a["puntos_fuertes"]:
                st.write(f"- {p}")
        with d:
            st.markdown("**👎 Puntos débiles**")
            for p in a["puntos_debiles"]:
                st.write(f"- {p}")
        st.info(f"**Recomendada para:** {a['recomendada_para']}")
        st.caption("La IA puede equivocarse con películas poco conocidas: verifica los datos.")

        if st.button("📡 Enviar a la pantalla de cine (Wokwi)"):
            if publicar("calificacion", f"{nota:.1f}") and publicar("titulo", a["titulo"]):
                st.success("Calificación enviada por MQTT. Míralo en 'Mi cine'.")
            else:
                st.error("No se pudo publicar en el broker MQTT.")

