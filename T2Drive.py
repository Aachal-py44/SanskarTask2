import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload

SCOPE = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'client_secret.json'
TOKEN_FILE = 'token.pickle'


def get_gdrive_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPE)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def upload_files():
    service = get_gdrive_service()

    folder_metadata = {"name": "Test", "mimeType": "application/vnd.google-apps.folder"}
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    folder_id = folder.get("id")
    print("Folder ID:", folder_id)

    file_metadata = {"name": "Test.pdf", "parents": [folder_id]}
    media = MediaFileUpload("Test.pdf", resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File uploaded, ID:", file.get("id"))


if __name__ == '__main__':
    upload_files()
