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

