import speech_recognition as sr
from langdetect import detect_langs

def transcribe_from_mic(timeout=5, phrase_time_limit=12):
    """
    Records from server microphone and returns:
    {
        "text": recognized_text,
        "lang": "hi" or "en"
    }
    """
    recognizer = sr.Recognizer()
    try:
        mic = sr.Microphone()
    except Exception as e:
        return {"error": f"Microphone not available: {e}"}

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Listening ...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return {"error": "Listening timed out — no speech detected."}

    # Try Hindi first, then English
    text_hi, text_en = "", ""
    try:
        text_hi = recognizer.recognize_google(audio, language="hi-IN")
    except:
        pass
    try:
        text_en = recognizer.recognize_google(audio, language="en-IN")
    except:
        pass

    # Pick the longer non-empty transcription
    if text_hi and len(text_hi) >= len(text_en):
        text = text_hi
    elif text_en:
        text = text_en
    else:
        try:
            text = recognizer.recognize_google(audio)
        except Exception as e:
            return {"error": f"Speech recognition failed: {e}"}

    # Language detection
    try:
        langs = detect_langs(text)
        if langs:
            primary = langs[0].lang
            lang_code = "hi" if primary.startswith("hi") else "en"
        else:
            lang_code = "en"
    except Exception:
        lang_code = "hi" if any(ch in text for ch in "अआइईउऊेो") else "en"

    return {"text": text, "lang": lang_code}
