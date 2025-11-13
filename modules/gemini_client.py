# modules/gemini_client.py
import os
from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not GEMINI_API_KEY:
        raise ValueError("Missing GEMINI_API_KEY")

    client = genai.Client(api_key=GEMINI_API_KEY)
    client_available = True
except Exception as e:
    print("⚠️ Gemini client not configured:", e)
    client = None
    client_available = False


def get_gemini_response(user_query: str, entities: dict, lang: str = "en") -> str:
    """
    Sends user query dynamically to Gemini LLM for English/Hindi response.
    """
    if not client_available:
        return "⚠️ Gemini client not configured. Check API key & package."

    # Choose language
    if lang == "hi":
        system_prompt = (
            "आप एक सहायक स्वास्थ्य सहायक हैं। उत्तर हिंदी में दें। "
            "मरीज के लक्षणों के आधार पर संभावित कारण, जांच, और सलाह दें। "
            "अगर ज़रूरी हो तो डॉक्टर से संपर्क करने की सलाह दें।"
        )
    else:
        system_prompt = (
            "You are a helpful healthcare assistant. Respond in English. "
            "Based on the patient's symptoms, suggest possible causes, recommended lab tests, and medicines if mild. "
            "Advise visiting a doctor when necessary."
        )

    # Combine context
    prompt = f"{system_prompt}\n\nUser Query: {user_query}\n\nDetected Entities: {entities}\n\nProvide a concise, clear, empathetic response."

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text.strip() if hasattr(response, "text") else str(response)
    except Exception as e:
        return f"⚠️ Error generating Gemini response: {e}"
