"""Simple command-line sample for the Calendar API.
Command-line application that retrieves the list of the user's calendars."""

import sys
from oauth2client import client
import codecs
from googleapiclient import sample_tools
import datetime


def main(argv):

    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope='https://www.googleapis.com/auth/calendar')

    try:
        page_token = None
        with open('file.txt' , 'w' , encoding="utf-8") as f:
            f.write(str(service.calendarList().list(pageToken=None).execute())) ; 
        
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()

            for calendar_list_entry in calendar_list['items']:
                if calendar_list_entry.get('primary'):
                    print(calendar_list_entry) ; 

            page_token = calendar_list.get('nextPageToken')

            if not page_token:
                break
        

    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')


if __name__ == '__main__':
    main(sys.argv)
