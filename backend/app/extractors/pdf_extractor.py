import fitz  # PyMuPDF library for extracting text from PDFs

def extract_pdf_text(file_path: str) -> str:
    """
    Extracts text from a PDF file using PyMuPDF (fitz).
    Returns one combined text string.
    """

    doc = fitz.open(file_path)                     # Open the PDF file
    full_text = ""                                 # Accumulator for all extracted text

    for page in doc:                               # Loop through each page
        text = page.get_text()                     # Extract clean text from the page
        full_text += text + "\n"                   # Append text to final output

    doc.close()                                    # Close the file to free memory
    return full_text                               # Return the complete extracted text
