import streamlit as st
from modules.speech_to_text import transcribe_from_mic
from modules.mcp_extractor import extract_entities
from modules.tts_response import tts_bytes
from modules.gemini_client import get_gemini_response
from langdetect import detect
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(page_title="Healthcare AI Assistant", layout="centered")
st.title("🩺 Healthcare Voice Assistant (Hindi & English)")
st.write("Speak or type your healthcare question (Hindi or English). Responses will be in English.")

col1, col2 = st.columns(2)
with col1:
    start_voice = st.button("🎤 Speak")
with col2:
    typed_query = st.text_input("Or type your question:")

# ===== Voice Input =====
if start_voice:
    res = transcribe_from_mic()
    if "error" in res:
        st.error(res["error"])
    else:
        user_text = res["text"]
        lang = res["lang"]
        st.success(f"🗣 You said: {user_text}")
        st.info(f"Detected language: {'Hindi' if lang=='hi' else 'English'}")

        entities = extract_entities(user_text)
        st.write("**Detected entities:**", entities)

        ai_response = get_gemini_response(user_text, entities, lang)
        st.subheader("💬 AI Response (English):")
        st.write(ai_response)

        audio_bytes = tts_bytes(ai_response, lang="en")
        st.audio(audio_bytes, format="audio/mp3")

# ===== Text Input =====
if typed_query and st.button("Ask (text)"):
    user_text = typed_query
    try:
        lang_code = detect(user_text)
        lang = "hi" if lang_code.startswith("hi") else "en"
    except:
        lang = "en"

    st.info(f"Detected language: {'Hindi' if lang=='hi' else 'English'}")

    entities = extract_entities(user_text)
    st.write("**Detected entities:**", entities)

    ai_response = get_gemini_response(user_text, entities, lang)
    st.subheader("💬 AI Response (English):")
    st.write(ai_response)

    audio_bytes = tts_bytes(ai_response, lang="en")
    st.audio(audio_bytes, format="audio/mp3")
