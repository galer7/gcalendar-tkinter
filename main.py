from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from utils import add_events, generate_calendar

from utils import do_folder_hash

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    changes_exist = False
    folder_hash = do_folder_hash()

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if not os.path.exists('persist.pickle'):
        with open('persist.pickle', 'wb') as f:
            print({"data": folder_hash})
            pickle.dump({"data": folder_hash}, f)

    else:
        with open('persist.pickle', 'rb') as f:
            data = pickle.load(f)
            print(data)

        if data != folder_hash:
            os.remove('token.pickle')

            with open('persist.pickle', 'wb') as f:
                pickle.dump({"data": folder_hash}, f)

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    events = generate_calendar()
    add_events(service, events=events,
               calendarId=r"aqtmhfl2bhjsicq2jd5cnnelhc@group.calendar.google.com")


if __name__ == '__main__':
    main()
    # print(do_folder_hash())
