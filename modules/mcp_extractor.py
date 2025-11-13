# modules/mcp_extractor.py
import re

def extract_entities(text: str) -> dict:
    """
    Lightweight entity extraction for symptoms, tests, medicines, and intent.
    """
    t = text.lower()
    entities = {
        "intent": None,
        "symptoms": [],
        "tests": [],
        "medicines": []
    }

    # Intent heuristics
    if any(w in t for w in ["test", "cbc", "lipid", "lab", "blood", "profile"]):
        entities["intent"] = "book_test"
    elif any(w in t for w in ["order", "dawai", "medicine", "tablet", "buy medicine"]):
        entities["intent"] = "order_medicine"
    elif any(w in t for w in ["doctor", "appointment", "consult"]):
        entities["intent"] = "consult_doctor"
    elif any(w in t for w in ["bukhar", "fever", "khansi", "cough", "pain", "headache"]):
        entities["intent"] = "symptom_check"
    else:
        entities["intent"] = "general_query"

    # Tests extraction (simple)
    found_tests = re.findall(r"(cbc|lipid profile|lipid|blood test|urine test|thyroid|sugar test)", t)
    if found_tests:
        entities["tests"] = list(set([x.upper() for x in found_tests]))

    # Medicines extraction (simple)
    found_meds = re.findall(r"(paracetamol|crocin|dolo|azithromycin|ibuprofen|antibiotic)", t)
    if found_meds:
        entities["medicines"] = list(set(found_meds))

    # Symptoms extraction
    found_symptoms = re.findall(r"(fever|bukhar|cough|cold|khansi|headache|nausea|vomiting|fatigue|weakness|pain)", t)
    if found_symptoms:
        entities["symptoms"] = list(set(found_symptoms))

    return entities
