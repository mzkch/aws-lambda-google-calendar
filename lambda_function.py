from __future__ import print_function

import datetime
import os

from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If you add a new custom module, add it to the create_lambda_function.sh script
from utils import send_slack_message

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# Calendar ID ***To be updated!!***
GOOGLE_CALENDAR_ID = os.environ.get('GOOGLE_CALENDAR_ID',
                                    'c_XXXXXXXXXXXXX@group.calendar.google.com')
# Google Calendar URL ***To be updated!!***
GOOGLE_CALENDAR_URL = os.environ.get('GOOGLE_CALENDAR_URL',
                                     'https://calendar.google.com/calendar/embed?src=c_XXXXX0group.calendar.google.com')

# Secret key path
KEY_PATH = './service_account_key.json'
# API name
API_NAME = 'calendar'
# API version
API_VERSION = 'v3'

# Slack webhook URL ***To be updated!!***
WEBHOOK_URL = os.environ.get('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/XXXXXX/YYYYYYY')


def main():
    # Import Service Account Key
    creds = service_account.Credentials.from_service_account_file(
        KEY_PATH, scopes=SCOPES)

    # Generate JWT token
    if not creds.valid:
        creds.refresh(Request())

    try:
        service = build(API_NAME, API_VERSION, credentials=creds)

        # Call the Calendar API
        now_utc = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        thirty_min_later_utc = (datetime.datetime.utcnow() + datetime.timedelta(minutes=30)).isoformat() + 'Z'

        print('Getting events between %s and %s' % (now_utc, thirty_min_later_utc))
        events_result = service.events().list(
            calendarId=GOOGLE_CALENDAR_ID,
            timeMin=now_utc, timeMax=thirty_min_later_utc,
            maxResults=5, singleEvents=True,
            orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            print(start, '->', end, event['summary'])

            send_slack_message(webhook_url=WEBHOOK_URL, pretext=event['summary'], title=event['summary'],
                               message=event['summary'])

        return

    except HttpError as error:
        print('An error occurred: %s' % error)


def lambda_handler(event, context):
    main()


if __name__ == '__main__':
    main()
