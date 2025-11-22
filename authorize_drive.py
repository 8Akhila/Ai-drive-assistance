from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle # converts the object into a byte stream and vice versa

# Google Drive read-only scope
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def main():
    creds = None

    # Load existing token if available
    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)

    # If no valid credentials exist, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save token
        with open("token.json", "wb") as token:
            pickle.dump(creds, token) # it is a function in python to serialize the object and save it to a file

    print("Google Drive authentication successful!")

if __name__ == "__main__":
    main()
