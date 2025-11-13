import re

# Extended lists
SYMPTOMS_LIST = [
    "fever","bukhar","cough","cold","khansi","headache","nausea","vomiting",
    "fatigue","weakness","pain","sore throat","dizziness","chills","diarrhea",
    "constipation","shortness of breath","breathlessness","body ache","joint pain",
    "muscle pain","stomach pain","loss of appetite","insomnia","anxiety","rash",
    "itching","heartburn","palpitations","sneezing","runny nose","swelling",
    "chest pain","back pain","eye pain","ear pain","throat irritation","urinary problem"
]

LAB_TESTS_LIST = [
    "cbc", "complete blood count", "lipid profile", "blood test", "urine test",
    "thyroid", "sugar test", "hba1c", "liver function", "kidney function",
    "x-ray", "ct scan", "mri", "ecg", "ultrasound", "stool test", "urine culture"
]

MEDICINES_LIST = [
    "paracetamol","crocin","dolo","azithromycin","ibuprofen","antibiotic",
    "antihistamine","cough syrup","vitamin c","multivitamin","pantoprazole",
    "omeprazole","metformin","insulin","amlodipine","losartan","atorvastatin",
    "prednisone","amoxicillin","ciprofloxacin"
]

def extract_entities(text: str) -> dict:
    """
    Extract healthcare entities: intent, symptoms, lab tests, medicines
    """
    t = text.lower()
    entities = {"intent": None, "symptoms": [], "tests": [], "medicines": []}

    # ---------- Intent detection ----------
    if any(w in t for w in ["test", "cbc", "lipid", "blood", "profile", "lab", "scan", "x-ray", "mri"]):
        entities["intent"] = "book_test"
    elif any(w in t for w in ["order", "dawai", "medicine", "tablet", "buy medicine", "prescription"]):
        entities["intent"] = "order_medicine"
    elif any(w in t for w in ["doctor", "appointment", "consult", "specialist"]):
        entities["intent"] = "consult_doctor"
    elif any(sym in t for sym in SYMPTOMS_LIST):
        entities["intent"] = "symptom_check"
    else:
        entities["intent"] = "general_query"

    # ---------- Test extraction ----------
    tests = [test.upper() for test in LAB_TESTS_LIST if test.lower() in t]
    if tests:
        entities["tests"] = list(set(tests))

    # ---------- Medicine extraction ----------
    meds = [med.upper() for med in MEDICINES_LIST if med.lower() in t]
    if meds:
        entities["medicines"] = list(set(meds))

    # ---------- Symptom extraction ----------
    symptoms = [sym for sym in SYMPTOMS_LIST if sym.lower() in t]
    if symptoms:
        entities["symptoms"] = list(set(symptoms))

    return entities
