import hashlib
import os
from pathlib import Path
import json
import time
import datetime

default_event = {
    'summary': 'Google I/O 2015',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2021-03-04T09:00:00+02:00',
        'timeZone': 'Europe/Bucharest',
    },
    'end': {
        'dateTime': '2021-03-04T17:00:00+02:00',
        'timeZone': 'Europe/Bucharest',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;INTERVAL=14;COUNT=2'
    ],
    'reminders': {
        'useDefault': True,
    },
}


def add_event(service, event=default_event, calendarId='primary'):
    event_response = service.events().insert(
        calendarId=calendarId, body=event).execute()
    print(f"Event created: {event_response.get('htmlLink')}")

    return event_response


def add_events(service, events=[default_event], calendarId='calendarId'):
    responses = []

    for event in events:
        res = add_event(service, event, calendarId=calendarId)
        responses.append(res)

    with open('added_events.json', 'w+') as f:

        # if file is empty, just put empty dict
        if len(f.readlines()) == 0:
            added_events = {}
        else:
            added_events = json.load(f)

        if calendarId not in added_events:
            added_events[calendarId] = {}

        added_events[calendarId][int(time.time())] = responses
        json.dump(added_events, f)


def get_events(service, number_of_events, calendarId='primary'):
    '''get first number_of_events from now'''
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=calendarId, timeMin=now,
                                          maxResults=number_of_events, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


def do_folder_hash(verbose=True):
    exclude_dirs = ['venv']
    hhash = hashlib.md5()
    dir_path = Path(__file__).parent.absolute()

    if not os.path.exists(dir_path):
        return -1

    try:
        for root, dirs, files in os.walk(dir_path):
            for exc in exclude_dirs:
                dirs[:] = [d for d in dirs if exc not in d]

            for file_name in files:
                filepath = os.path.join(root, file_name)
                if verbose == True:
                    print(f"Hashing {filepath}")
                try:
                    with open(filepath, 'rb') as f:
                        while True:
                            # Read file in as little chunks
                            buf = f.read(4096)
                            if not buf:
                                break
                            hhash.update(buf)
                except:
                    continue

    except:
        import traceback
        # Print the stack traceback
        traceback.print_exc()
        return -2

    return hhash.hexdigest()


class Date:
    start = current = "2021-03-01"
    start_datetime = current_datetime = datetime.date(
        *[int(x) for x in start.split('-')])

    def add_one():
        next_day = Date.current_datetime + datetime.timedelta(days=1)

        while next_day.weekday() >= 5:
            next_day += datetime.timedelta(days=1)

        Date.current_datetime = next_day

    def get_date_str():
        year = Date.current_datetime.year
        month = str(Date.current_datetime.month).zfill(2)
        day = str(Date.current_datetime.day).zfill(2)

        return f"{year}-{month}-{day}"


def romanian_event(title, date, start, end):
    return {
        'summary': title,
        'start': {
            'dateTime': str(date) + 'T' + str(start).zfill(2) + ':00:00+02:00',
            'timeZone': 'Europe/Bucharest',
        },
        'end': {
            'dateTime': str(date) + 'T' + str(end).zfill(2) + ':00:00+02:00',
            'timeZone': 'Europe/Bucharest',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;INTERVAL=14;COUNT=7'
        ],
        'reminders': {
            'useDefault': True,
        },
    }


def generate_calendar():
    events = []
    with open('./calendar.json', 'r') as f:
        structure = json.load(f)
        for key in structure.keys():

            print(Date.get_date_str())
            for event in structure[key]:
                events.append(romanian_event(
                    **event, date=Date.get_date_str()))

            Date.add_one()

    with open('./output_events.json', 'w') as f:
        json.dump(events, f)

    return events
