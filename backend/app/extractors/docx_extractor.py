# backend/app/extractors/docx_extractor.py

import docx

def extract_docx_text(path: str) -> str:
    """
    Read a .docx file and return its text content.
    This is the function name used by the Extractor system.
    """
    try:
        document = docx.Document(path)
        return "\n".join([paragraph.text for paragraph in document.paragraphs])
    except Exception as e:
        print(f"❌ DOCX extraction failed: {e}")
        return ""
