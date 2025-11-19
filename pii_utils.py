import re

def mask_pii(text: str) -> str:
    if not text:
        return text

    # email
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', text)

    # phone number
    text = re.sub(r'\b05[0-9]-?[0-9]{7}\b', '[PHONE]', text)

    # id
    text = re.sub(r'\b\d{9}\b', '[ID_NUMBER]', text)

    # card (Visa/MasterCard)
    text = re.sub(r'\b(?:\d[ -]*?){13,16}\b', '[CREDIT_CARD]', text)

    # dates (dd/mm/yyyy)
    text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{4}\b', '[DATE]', text)

    return text
