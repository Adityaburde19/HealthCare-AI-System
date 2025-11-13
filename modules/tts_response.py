# modules/tts_response.py
from gtts import gTTS
from io import BytesIO

def tts_bytes(text: str, lang: str = "en") -> bytes:
    """
    Convert text to speech using gTTS and return MP3 bytes.
    This avoids temp file permission issues on Windows.
    """
    gt_lang = "hi" if lang == "hi" else "en"
    mp3_fp = BytesIO()
    tts = gTTS(text=text, lang=gt_lang)
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    return mp3_fp.read()
