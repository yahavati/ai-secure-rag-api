import PyPDF2
import docx
from io import BytesIO

def pdf_to_text(file_bytes: bytes) -> str:
    """
    Convert PDF bytes to text.
    """
    reader = PyPDF2.PdfReader(BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    return text


def docx_to_text(file_bytes: bytes) -> str:
    """
    Convert DOCX bytes to text.
    """
    doc = docx.Document(BytesIO(file_bytes))
    return "\n".join([p.text for p in doc.paragraphs])


def convert_to_text(filename: str, file_bytes: bytes) -> str:
    """
    Main function that decides how to convert a file to text.
    Supports: PDF, DOCX.
    """
    if filename.lower().endswith(".pdf"):
        return pdf_to_text(file_bytes)

    elif filename.lower().endswith(".docx"):
        return docx_to_text(file_bytes)

    else:
        raise ValueError("Unsupported file type. Only PDF and DOCX are allowed.")
