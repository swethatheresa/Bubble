import googleapiclient
import sys

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

scopes=['https://www.googleapis.com/auth/calendar']
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json",scopes=scopes)
credentials=flow.run_console()
import pickle
pickle.dump(credentials,open("cal_cred.pkl","wb"))
#credentials=pickle.load(open("cal_cred.pkl","rb"))
service=build("calendar","v3",credentials=credentials)

result = service.calendarList().list().execute()
user_calendar_id=result['items'][0]['id']
res=service.events().list(calendarId=user_calendar_id).execute()
from datetime import datetime,timedelta
start_time=datetime(year,month,date)
topic=
event = {
  'summary': topic,
  'location': 'none',
  'description': 'none',
  'start': {
    # 'dateTime': start_time.strftime("%Y-%m-&dT12:00:00"),
    'dateTime': '2022-12-24T09:00:00-07:00',
    'timeZone': 'Asia/Kolkata',
  },
  'end': {
    #'dateTime': end_time.strftime("%Y-%m-&dT%12:30:00"),
    'dateTime': '2022-12-24T10:00:00-07:00',
    'timeZone': 'Asia/Kolkata',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=2'
  ],
  'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
service.events().insert(calendarId='sinta.paul39@gmail.com',body=event).execute()