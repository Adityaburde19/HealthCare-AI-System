# modules/speech_to_text.py
import speech_recognition as sr
from langdetect import detect_langs

def transcribe_from_mic(timeout=5, phrase_time_limit=12):
    """
    Records from server microphone and returns tuple (text, detected_language_code)
    detected_language_code: 'hi' or 'en' (fallback 'en' if uncertain)
    """
    recognizer = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()
    except Exception as e:
        return {"error": f"Microphone not available: {e}"}

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Listening (server mic) ...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return {"error": "Listening timed out — no speech detected."}

    # Try Hindi first then English; aggregate best result
    text_hi = ""
    text_en = ""
    try:
        text_hi = recognizer.recognize_google(audio, language="hi-IN")
    except Exception:
        text_hi = ""

    try:
        text_en = recognizer.recognize_google(audio, language="en-IN")
    except Exception:
        text_en = ""

    # Choose the non-empty longer transcription
    if text_hi and (len(text_hi) >= len(text_en)):
        text = text_hi
    elif text_en:
        text = text_en
    else:
        # final fallback - try generic recognize_google
        try:
            text = recognizer.recognize_google(audio)
        except Exception as e:
            return {"error": f"Speech recognition failed: {e}"}

    # Language detection from text (langdetect)
    try:
        langs = detect_langs(text)
        # detect_langs returns list like [en:0.99] or [hi:0.95]
        if langs:
            primary = langs[0].lang
            if primary.startswith("hi"):
                lang_code = "hi"
            else:
                lang_code = "en"
        else:
            lang_code = "en"
    except Exception:
        lang_code = "hi" if any(ch in text for ch in "अआइईउऊेो") else "en"

    return {"text": text, "lang": lang_code}
