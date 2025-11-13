# app.py
import streamlit as st
import speech_recognition as sr
from langdetect import detect
from dotenv import load_dotenv
import os
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO

# ==================== Load environment variables ====================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
genai.configure(api_key=GOOGLE_API_KEY)

# ==================== Streamlit UI ====================
st.set_page_config(page_title="Healthcare Voice Assistant", layout="centered")
st.title("🩺 Healthcare Voice Assistant (Hindi & English)")

st.write("Click the button below and speak your healthcare question (Hindi or English).")
st.write("You can also type your question in the input box.")

# ==================== Initialize recognizer ====================
recognizer = sr.Recognizer()

# ==================== Functions ====================

def record_and_recognize():
    """Record from server microphone and return recognized text"""
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Speak now!")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
        except sr.WaitTimeoutError:
            return {"error": "Listening timed out, no speech detected."}

    try:
        # Try Hindi first
        text_hi = recognizer.recognize_google(audio, language="hi-IN")
    except:
        text_hi = ""
    try:
        # Then English
        text_en = recognizer.recognize_google(audio, language="en-IN")
    except:
        text_en = ""

    # Choose longer transcription
    if len(text_hi) >= len(text_en):
        text = text_hi if text_hi else text_en
    else:
        text = text_en

    if not text:
        return {"error": "Could not understand the audio."}

    # Detect language
    try:
        lang_code = detect(text)
        lang = "hi" if lang_code.startswith("hi") else "en"
    except:
        lang = "en"

    return {"text": text, "lang": lang}

def get_gemini_response(user_query, lang="en"):
    """Call Gemini API to get response in same language"""
    model = genai.GenerativeModel("gemini-2.5-flash")  # Change if needed
    prompt = f"You are a helpful healthcare assistant. Answer the following query in {lang}:\n{user_query}"
    try:
        response = model.generate_content(prompt)
        reply = response.text
        return reply
    except Exception as e:
        return f"⚠️ Error fetching response: {e}"

def tts_bytes(text, lang="en"):
    """Convert text to speech and return bytes for Streamlit audio"""
    gt_lang = "hi" if lang == "hi" else "en"
    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang=gt_lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp.read()

# ==================== Streamlit logic ====================

col1, col2 = st.columns(2)

with col1:
    start_voice = st.button("🎤 Speak")

with col2:
    typed_query = st.text_input("Or type your question here:")

# ===== Voice input =====
if start_voice:
    res = record_and_recognize()
    if "error" in res:
        st.error(res["error"])
    else:
        user_text = res["text"]
        lang = res["lang"]
        st.success(f"🗣 You said: {user_text}")
        st.info(f"Detected language: {'Hindi' if lang=='hi' else 'English'}")

        # Gemini response
        with st.spinner("Getting response from Gemini..."):
            ai_response = get_gemini_response(user_text, lang)
        st.subheader("💬 AI Response:")
        st.write(ai_response)

        # Play TTS
        audio_bytes = tts_bytes(ai_response, lang)
        st.audio(audio_bytes, format="audio/mp3")

# ===== Text input =====
if typed_query and st.button("Ask (text)"):
    user_text = typed_query
    try:
        lang_code = detect(user_text)
        lang = "hi" if lang_code.startswith("hi") else "en"
    except:
        lang = "en"

    st.info(f"Detected language: {'Hindi' if lang=='hi' else 'English'}")
    ai_response = get_gemini_response(user_text, lang)
    st.subheader("💬 AI Response:")
    st.write(ai_response)
    audio_bytes = tts_bytes(ai_response, lang)
    st.audio(audio_bytes, format="audio/mp3")
