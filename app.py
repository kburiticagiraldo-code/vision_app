import os
import streamlit as st
import base64
from openai import OpenAI

# Función para codificar la imagen a base64
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode("utf-8")

st.set_page_config(page_title="Cinéfilo IA - Reseñas de Películas y Series", layout="centered", initial_sidebar_state="collapsed")

# Configuración de la interfaz de la página
st.title("🎬 Tu Crítico de Cine Personal con IA")
st.markdown("Sube la captura o el póster de una película o serie y recibe una reseña a tu medida.")

# Inicializamos el cliente de OpenAI usando los Secrets de Streamlit Cloud de forma automática
try:
    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)
except Exception:
    st.error("⚠️ No se encontró la clave `OPENAI_API_KEY` en los Secrets de Streamlit. Por favor configúrala en el panel de administración.")
    client = None

# Campo para que el usuario ingrese sus gustos cinematográficos
user_tastes = st.text_input(
    "¿Cuáles son tus géneros, directores o actores favoritos?",
    placeholder="Ej: Me encantan las de ciencia ficción, Christopher Nolan y las series de misterio."
)

# Selector de archivo para subir la imagen de la película o serie
uploaded_file = st.file_uploader("Sube una imagen de la película o serie (póster o escena)", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.expander("Imagen cargada", expanded=True):
        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)

# Toggle para agregar un comentario adicional si se desea
show_details = st.toggle("¿Quieres agregar algún comentario extra sobre qué esperas ver?", value=False)
additional_details = ""
if show_details:
    additional_details = st.text_area("Escribe tus expectativas o dudas sobre esta obra:")

# Botón para generar la reseña
analyze_button = st.button("Generar Reseña Personalizada", type="primary")

# Lógica principal al hacer clic en el botón
if analyze_button:
    if not uploaded_file:
        st.warning("Por favor, sube la imagen de una película o serie.")
    elif client is None:
        st.error("La aplicación no se pudo conectar con OpenAI debido a un problema con la clave.")
    else:
        with st.spinner("Analizando la imagen y redactando tu reseña cinéfila..."):
            # Codificar la imagen
            base64_image = encode_image(uploaded_file)
        
            # Construir un prompt enfocado en cine, series y los gustos del usuario
            prompt_text = (
                "Actúa como un crítico de cine y televisión experto, apasionado y muy entretenido. "
                "Analiza la imagen adjunta, identifica de qué película o serie se trata (póster o escena). "
                "Luego, redacta una reseña crítica y atractiva de esta obra. "
            )
            
            if user_tastes:
                prompt_text += f"\n\nTen muy en cuenta los gustos del usuario para adaptar la reseña: '{user_tastes}'. Conecta si esta obra le va a encantar o no basándote en esto."
            
            if show_details and additional_details:
                prompt_text += f"\n\nComentario adicional del usuario: {additional_details}"
                
            prompt_text += "\n\nEscribe tu respuesta completa en español de manera fluida."
        
            # Estructurar los mensajes para GPT-4o
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        },
                    ],
                }
            ]
        
            # Hacer la petición a la API de OpenAI con streaming
            try:
                full_response = ""
                message_placeholder = st.empty()
                for completion in client.chat.completions.create(
                    model="gpt-4o", 
                    messages=messages,    
                    max_tokens=1500, 
                    stream=True
                ):
                    if completion.choices[0].delta.content is not None:
                        full_response += completion.choices[0].delta.content
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
        
            except Exception as e:
                st.error(f"Ocurrió un error al procesar la solicitud: {e}")
