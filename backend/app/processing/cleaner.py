import re   # Regex library for cleaning unwanted patterns

def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing extra spaces, non-printable chars,
    bad line breaks, and repeated whitespace.
    """

    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove non-printable characters (like control characters)
    text = re.sub(r"[^\x20-\x7E\n]", "", text)

    # Strip leading and trailing whitespace
    text = text.strip()

    return text  # Return the cleaned text
