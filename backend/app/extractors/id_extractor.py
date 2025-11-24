# backend/app/analysis/id_extractor.py
"""
Utility to detect structured IDs (Aadhaar, PAN, etc.) from text.
You can extend this with more patterns later.
"""

import re
from typing import Dict, List

# Aadhaar: 4 4 4 digits with spaces
AADHAAR_REGEX = re.compile(r"\b\d{4}\s\d{4}\s\d{4}\b")

# PAN: 5 letters, 4 digits, 1 letter (simple pattern)
PAN_REGEX = re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b")

def extract_ids(text: str) -> Dict[str, List[str]]:
    """
    Scan the given text and return a dict of detected ID values.
    Example:
    {
        "aadhaar": ["1234 5678 9012"],
        "pan": ["ABCDE1234F"]
    }
    """

    ids: Dict[str, List[str]] = {}

    # Aadhaar matches
    aadhaar_matches = AADHAAR_REGEX.findall(text)
    if aadhaar_matches:
        ids["aadhaar"] = list(set(aadhaar_matches))  # unique values

    # PAN matches (uppercase only; make sure text is uppercased first below)
    upper_text = text.upper()
    pan_matches = PAN_REGEX.findall(upper_text)
    if pan_matches:
        ids["pan"] = list(set(pan_matches))

    return ids
