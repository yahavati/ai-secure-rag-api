from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

#making a secret key
SECRET = os.getenv("SECRET")

DANGEROUS_QUERY_PATTERNS = [
    "ignore", "bypass", "override",
    "show me the raw document",
    "print the entire file",
    "reveal", "expose"
]

def is_malicious_query(q: str) -> bool:
    for p in DANGEROUS_QUERY_PATTERNS:
        if p.lower() in q.lower():
            return True
    return False

def ai_sensitive_check(text: str) -> str:
    prompt = f"""
    Analyze the following document ONLY for sensitive data.

    Sensitive data includes:
    - phone numbers
    - emails
    - ID numbers
    - passwords / API keys
    - medical or private personal data

    Respond with EXACTLY one word:
    SAFE  (no sensitive data)
    UNSAFE  (contains sensitive data)

    Document:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content.strip().upper()

    # ננקה תווים עודפים
    answer = answer.replace(".", "").replace(":", "").strip()

    # נוודא שרק SAFE/UNSAFE נשאר
    if "UNSAFE" in answer:
        return "UNSAFE"
    if "SAFE" in answer:
        return "SAFE"

    # fallback: אם לא ברור → נזהרים
    return "UNSAFE"

def is_document_safe(text: str) -> bool:
    return ai_sensitive_check(text) == "SAFE"


