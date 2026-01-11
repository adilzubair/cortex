import pdfplumber
from docx import Document as DocxDocument
from .base import IngestedDocument

def load_pdf(path: str):
    docs = []
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or "" for page in pdf.pages)

    docs.append(
        IngestedDocument(
            content=text,
            metadata={"type": "pdf", "path": path}
        )
    )
    return docs
