# modules/gemini_client.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Try to import genai safely
try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    client_available = True
except Exception as e:
    print("Warning: google.generativeai not available or failed to import:", e)
    genai = None
    client_available = False

def get_gemini_response(user_query: str, entities: dict, lang: str = "en") -> str:
    """
    Sends prompt to Gemini and requests a reply in the given language ('en' or 'hi').
    Returns text response or an error message.
    """
    # Prepare instruction to respond in same language
    if lang == "hi":
        system_prompt = "आप एक सहायक स्वास्थ्य (healthcare) बॉट हैं। उत्तर हिंदी में दें। सीमित दवाइयों का सुझाव न दें; अगर आवश्यक हो तो डॉक्टर से मिलने के निर्देश दें।"
        user_prefix = f"उपयोगकर्ता का प्रश्न: {user_query}\n\nपहचान की गई जानकारी: {entities}"
    else:
        system_prompt = "You are a helpful healthcare assistant. Respond in English. Do not prescribe strong medications; advise consulting a doctor when needed."
        user_prefix = f"User query: {user_query}\n\nDetected entities: {entities}"

    prompt = system_prompt + "\n\n" + user_prefix + "\n\nProvide a clear, empathetic short reply."

    if not client_available:
        return "⚠️ Gemini client not configured. Check GOOGLE/GEMINI SDK and API key."

    try:
        # SDK usage may vary by installed version; try a robust call:
        response = genai.generate_text(model=GEMINI_MODEL, prompt=prompt, temperature=0.0, max_output_tokens=400)
        # response may be a dict or object depending on genai version
        if hasattr(response, "text"):
            return response.text
        if isinstance(response, dict):
            # try common keys
            return response.get("content") or response.get("text") or str(response)
        return str(response)
    except Exception as e:
        # try alternate call pattern for some genai versions
        try:
            client = genai.Client()
            out = client.models.generate_content(model=GEMINI_MODEL, contents=[{"type":"text","text":prompt}], temperature=0.0)
            if hasattr(out, "text"):
                return out.text
            return str(out)
        except Exception as e2:
            return f"⚠️ Error fetching response: {e} / {e2}"
