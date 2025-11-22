import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from backend.app.config import settings

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_drive_service():
    """
    Safely creates and returns an authenticated Google Drive client.
    Handles:
        ✔ token.json (valid or expired)
        ✔ corrupted tokens
        ✔ Windows encrypted/binary tokens
        ✔ fresh OAuth login
    """

    creds = None

    # 1) LOAD EXISTING TOKEN
    if os.path.exists(settings.GOOGLE_TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(
                settings.GOOGLE_TOKEN_PATH, SCOPES
            )
        except Exception:
            # Token invalid or encrypted → force login
            creds = None

    # 2) VALIDATE OR REFRESH
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None  # fallback to full login
        if creds is None or not creds.valid:
            # 3) FRESH LOGIN FLOW
            flow = InstalledAppFlow.from_client_secrets_file(
                settings.GOOGLE_CREDENTIALS_PATH,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        # 4) SAVE TOKEN
        with open(settings.GOOGLE_TOKEN_PATH, "w") as token:
            token.write(creds.to_json())

    # 5) RETURN DRIVE SERVICE
    from googleapiclient.discovery import build
    return build("drive", "v3", credentials=creds)
