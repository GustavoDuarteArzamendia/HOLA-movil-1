
import streamlit as st
from gtts import gTTS
from deep_translator import GoogleTranslator
import base64
import os
import tempfile

st.set_page_config(page_title="HOLA Traductor", layout="centered")

logo_path = "hola_icon_android.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        logo_bytes = f.read()
        logo_b64 = base64.b64encode(logo_bytes).decode()
        st.markdown(f'''
            <div style='text-align: center;'>
                <img src='data:image/png;base64,{logo_b64}' width='150'/>
                <h1 style='color:#ff6600;'>HOLA</h1>
                <h4>Traducción por voz con detección de idioma</h4>
            </div>
        ''', unsafe_allow_html=True)

texto = st.text_area("🎤 Escribí o pegá tu texto", height=150)

idiomas = {
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Portugués": "pt",
    "Chino": "zh-CN",
    "Español": "es"
}

idioma_destino = st.selectbox("🌍 Elegí idioma destino", list(idiomas.keys()))

if st.button("🔄 Traducir y reproducir"):
    if texto:
        try:
            idioma_origen = GoogleTranslator(source='auto', target=idiomas[idioma_destino]).detect(texto)
            traduccion = GoogleTranslator(source='auto', target=idiomas[idioma_destino]).translate(texto)
            st.success(f"Traducción: {traduccion}")

            tts = gTTS(traduccion, lang=idiomas[idioma_destino])
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                audio_path = fp.name

            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')

            os.remove(audio_path)

        except Exception as e:
            st.error("❌ Ocurrió un error al procesar tu solicitud.")
    else:
        st.warning("⚠️ Ingresá un texto para traducir.")
