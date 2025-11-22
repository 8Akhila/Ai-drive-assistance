# Utility helpers used for Google Drive file processing.
# These are simple helper functions used across the sync and extraction flow.

import mimetypes      # Helps detect file types from names


def get_file_extension(filename: str):
    """
    Returns the file extension from a filename.
    Example: 'resume.pdf' -> '.pdf'
    """
    return filename.lower().split(".")[-1]


def is_supported_file(filename: str):
    """
    Checks if a file format is supported by the AI agent.
    Supported formats include:
    - pdf
    - docx
    - images (png, jpg)
    - videos (mp4, mov)
    """

    ext = get_file_extension(filename)

    supported = ["pdf", "docx", "png", "jpg", "jpeg", "mp4", "mov", "mkv"]

    return ext in supported


def guess_mime_type(filename: str):
    """
    Returns MIME type of a file.
    Example: resume.pdf -> application/pdf
    """
    return mimetypes.guess_type(filename)[0]
