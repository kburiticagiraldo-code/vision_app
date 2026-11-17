import streamlit as st

from estilo import aplicar_estilo, hero

st.set_page_config(page_title="Crítico de cine IA", page_icon="🎬", layout="centered")
aplicar_estilo()

hero(
    "Crítico de cine IA",
    "Identifica tu película con IA y deja que tu pantalla de cine en Wokwi te muestre el veredicto.",
    "🎬",
)

st.markdown("### ¿Cómo funciona?")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(
        '<div class="paso"><span class="paso-num">1</span>'
        '<div class="paso-titulo">🍿 Analiza</div>'
        '<div class="paso-texto">Escribe el título o sube el póster. La IA reconoce la película, '
        "te da su reseña crítica y una calificación final.</div></div>",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        '<div class="paso"><span class="paso-num">2</span>'
        '<div class="paso-titulo">📡 Conecta</div>'
        '<div class="paso-texto">Envía esa calificación al dispositivo simulado en Wokwi (ESP32) '
        "por MQTT, en ambos sentidos.</div></div>",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        '<div class="paso"><span class="paso-num">3</span>'
        '<div class="paso-titulo">⭐ Veredicto</div>'
        '<div class="paso-texto">Mira la calificación en tiempo real. Los LEDs te dicen si '
        "vale la pena verla, si es regular o si es mejor saltársela.</div></div>",
        unsafe_allow_html=True,
    )

st.write("")
b1, b2 = st.columns(2)
with b1:
    st.page_link("pages/1_Analizar_pelicula.py", label="Analizar película", icon="🎞️")
with b2:
    st.page_link("pages/2_Mi_cine.py", label="Ver mi dispositivo", icon="📡")
