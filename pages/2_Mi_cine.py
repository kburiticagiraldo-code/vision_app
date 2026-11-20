import streamlit as st

from estilo import aplicar_estilo, hero
from mqtt_utils import PREFIJO, leer_estado, veredicto

st.set_page_config(page_title="Mi cine", page_icon="📡", layout="centered")
aplicar_estilo()
hero("Mi cine", "Tu dispositivo ESP32 en Wokwi, conectado por MQTT en ambos sentidos.", "📡")

ESTADOS = {
    "ver": "🟢 Vale la pena verla",
    "regular": "🟡 Regular",
    "saltar": "🔴 Mejor sáltala",
}


@st.fragment(run_every=3)
def panel():
    datos = leer_estado()
    if datos is None:
        st.error("No se pudo conectar al broker MQTT.")
        return
    if not datos:
        st.info("Aún no hay mensajes. Analiza una película y envíala, y arranca la simulación en Wokwi.")
        return

    st.markdown(f"### 🎞️ {datos.get('titulo', 'Sin película enviada')}")
    c1, c2, c3 = st.columns(3)

    nota = datos.get("calificacion")
    c1.metric("Nota de la IA", f"{float(nota):.1f}" if nota else "—")
    c2.metric("LED en Wokwi", ESTADOS.get(datos.get("estado"), "Sin respuesta"))
    mi = datos.get("mi_nota")
    c3.metric("Tu nota (potenciómetro)", f"{float(mi):.1f}" if mi else "—")

    if nota and mi:
        dif = float(mi) - float(nota)
        st.write(f"Tu nota está **{abs(dif):.1f}** puntos {'por encima' if dif >= 0 else 'por debajo'} de la del crítico.")
    st.caption(f"Actualiza cada 3 s · tema base MQTT: `{PREFIJO}/…`")


panel()

st.markdown("### Cómo probarlo")
st.markdown(
    "1. Abre tu proyecto en Wokwi y pulsa **Start**.\n"
    "2. Analiza una película y pulsa **Enviar a la pantalla de cine**.\n"
    "3. Los LEDs cambian y aquí ves la respuesta. Gira el potenciómetro para poner tu propia nota."
)
