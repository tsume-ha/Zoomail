import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from django.conf import settings

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events',
    ]

def createService():
    # creds = None
    # # The file token.pickle stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    pickle_path = os.path.join(settings.BASE_DIR, 'token.pickle')
    json_path = os.path.join(settings.BASE_DIR, 'credentials.json')
    # print(pickle_path)
    # if os.path.exists(pickle_path):
    #     with open(pickle_path, 'rb') as token:
    #         creds = pickle.load(token)
    # # If there are no (valid) credentials available, let the user log in.
    # if not creds or not creds.valid:
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             json_path, SCOPES)
    #         creds = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open(pickle_path, 'wb') as token:
    #         pickle.dump(creds, token)


    credentials = service_account.Credentials.from_service_account_file(
            json_path, scopes=SCOPES)

    return build('calendar', 'v3', credentials=credentials)