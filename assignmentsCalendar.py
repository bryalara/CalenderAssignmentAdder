from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import csv
from parse import *

def readCSV():
    # file= input("Enter csv file name: ")
    file="test.csv"
    assignments=[]
    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        lineCount=0
        for row in csv_reader:
            if lineCount == 0:
                print(f'Column names are {",".join(row)}')
                lineCount += 1
            else:
                assignments= assignments + [row]
                print(f"\tAssignment: {row[0]} is due on {row[1]} at "+ (str(row[2]) if row[2]!="" else "11:59 pm") )
                if row[2]=="":
                    row[2]="11:59 pm"
                lineCount += 1
        print(f'Total assignments: {lineCount}.')
        return assignments

def formatEvents(assignments):
    formattedEvents=[]
    parsedDate=[]
    parsedTime=[]

    for elem in assignments:
        formattedTime=""
        inputDate=elem[1]
        inputTime= elem[2]

        #format inputDate
        parsingDate =parse("{MM}/{DD}/{YYYY}", inputDate)
        parsedDate = [parsingDate['MM'] , parsingDate['DD'], parsingDate ['YYYY'] ]
        if len(parsedDate[0])==1:
            parsedDate[0]= "0"+parsedDate[0]
        if len(parsedDate[1])==1:
            parsedDate[1]= "0"+parsedDate[0]
        reorganizedDate= parsedDate[2]+"-"+parsedDate[1]+"-"+parsedDate[0]

        #format inputTime
        parsingTime = parse("{HR}:{MIN} {T}", inputTime)
        parsedTime= [parsingTime['HR'] , parsingTime['MIN'], parsingTime ['T'] ]
        if parsedTime[2]=="pm":
            parsedTime[0]= str(12+int(parsedTime[0]))
        else:
            if len(parsedTime[0])==1:
                parsedTime[0]= "0"+parsedTime[0]
        reorganizedTime= parsedTime[0]+":"+parsedTime[1]
        # endTimeMin=str( int(parsedTime[1]) + 1)
        # endTimeHr=parsedTime[0]
        # if (endTimeMin=="60"):
        #     endTimeMin="00"
        #     endTimeHr=str(int(endTimeHr)+1)
        #     if endTimeHr=="24":
        #         endTimeHr="00"
        # finalEndTime=endTimeHr+endTimeMin

        formattedTime= reorganizedDate +"T"+reorganizedTime+"-5:00"

        formattedEvents= formattedEvents + [[formattedTime, elem[0]]]
    return formattedEvents

def chooseUserCal():
    print("Getting user's calendars")
    calList = service.calendarList().list().execute()
    items= calList.get('items',[])
    count=1
    calendars=[]
    for item in items:
        calendars=calendars + [item]
        cal= item['summary']
        print(str(count) +" "+cal)
        count=count+1
    choice= int(input("Which calendar would you like to insert events into?\n"))
    calendarChosen= calendars[choice-1]
    return calendarChosen

#intial variable settup
assignments=[]
csvReady=False

#reading input CSV
while not csvReady:
    assignments=readCSV()
    # proceed = input("is this correct? (Y/N)\n")
    # if (proceed=="Y" or proceed=="y"):
    #     csvReady=True
    csvReady=True

#CSV data ready, now need to modify for calendar input
#needed format [event time(year-month-day-THR:MIN-HR:MIN), name]
assignments=formatEvents(assignments)

#initialize calendar api
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
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

userCal= chooseUserCal()
print(userCal)




