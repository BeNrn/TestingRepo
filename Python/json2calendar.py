# -*- coding: utf-8 -*-
"""
Purpose:    Trasform JSON to VCS (vCalendar-Format) resp. ICS file.
Created:    24.11.2024
Creator:    BeNrn 
"""
#from https://github.com/eoleedi/TimeTree-exporter
#go to https://timetreeapp.com/signin
#open developer tools in the browser
#go to networks tab
#go to edits of the network tabs and select: Do not delete the logs
#type in the search bar "sync"
#sign in
#the first file is called "sync" but it can only hold a specific amount of data
# if it is more than that amount, more sync files will be generated being named something like "sync?since=16..."
#store those files on your device
#add the .json ending to each file
# (open in VS Code, type in >Format Document)

#import libs
#-----------
import json
import datetime

#set variables
#-------------
#file path
file_path = r"...\sync.json"
output_path = r"...\calender"

#set header and footer
header = """BEGIN:VCALENDAR
VERSION:2.0
"""
footer = """END:VCALENDAR"""

#define the output type
ics = True

if ics:
    file_ending = ".ics"
else:
    file_ending = ".vcs"
    
#concatenate the output file name
ouput_file_path = output_path + file_ending

#convert an event from JSON to calendar format
#-----------------------------------------------
def event_to_vcs(event):
    
    #define variables
    recurrences = event['recurrences']
    all_day = event["all_day"]
    event_start = event['start_at']
    event_end = event['end_at']
    
    #set recurrences
    #----------------
    if recurrences == []:
        recurrences = ""
    else:
        recurrences = event['recurrences'][0]
    
    #check for all day events
    #------------------------
    if all_day and len(recurrences) == 8:
        if ics:
            recurrences = recurrences + "T000000Z" #add time
        else:
            recurrences = recurrences + "T000000" #add time
    
    #set start and end date
    #-----------------------
    event_start = event_start/ 1000 #from miliseconds to seconds
    event_end = event_end / 1000
    
    event_start = datetime.datetime.fromtimestamp(event_start, datetime.timezone.utc) #Return the UTC datetime
    event_end = datetime.datetime.fromtimestamp(event_end, datetime.timezone.utc)
    
    #timetree shifts the date of recurrent events by 1 hour
    if recurrences != "":
        event_start = event_start + datetime.timedelta(hours=1)
        event_end = event_end + datetime.timedelta(hours=1)
    
    #check for whole day events
    if event["all_day"]:
        event_start = event_start.strftime('%Y%m%d') + "T000000" #to VCS format
        event_end = event_end.strftime('%Y%m%d') + "T240000"
    else:
        event_start = event_start.strftime('%Y%m%dT%H%M%S') + "Z" #to VCS format
        event_end = event_end.strftime('%Y%m%dT%H%M%S') + "Z"
            
    
    # vCalendar-Format
    if recurrences == "":
        vcs_data = f"""BEGIN:VEVENT
        LOCATION:{event['location']}
        SUMMARY:{event['title']}
        DESCRIPTION:{event['note']}
        DTSTART:{event_start}
        DTEND:{event_end}
        END:VEVENT
        """
    else:
        vcs_data = f"""BEGIN:VEVENT
        LOCATION:{event['location']}
        SUMMARY:{event['title']}
        DESCRIPTION:{event['note']}
        DTSTART:{event_start}
        DTEND:{event_end}
        {recurrences}
        END:VEVENT
        """
    return vcs_data

#load the json file
with open(file_path, "r") as file:
    events = json.load(file)

#create the calendar file
with open(ouput_file_path, "w") as file:
    file.write(header)
    for event in events["events"]:
        vcs_event = event_to_vcs(event)
        #file.write(vcs_event + "\n")
        file.write(vcs_event.replace("        ", ""))#remove white spaces
    file.write(footer)

##########
#bei outlook web anmelden
# Kalender hinzufügen
# from file

#VCALENDAR KNOW HOW
#https://karlrege.internet-box.ch/~rege/archive/dnet_hs13/dnet8/R25v33_understanding_vcal.pdf
#---------------------------------------------------------------------------------------------
"""
BEGIN:VCALENDAR                             vCalendar object properties
METHOD:REQUEST                              vCalendar object properties
VERSION:1.0                                 vCalendar object properties
PRODID:-//Intrfc//NONSGML Intrfc//EN        vCalendar object properties
BEGIN:VEVENT                                Beginning of vEvent object
UID:FA05003244                              Class unique identifier
SUMMARY:ACC101                              Class name
SEQUENCE:1                                  1 indicates new class
ATTENDEE;ROLE=INSTRUCTOR:jdoe@myu.edu       Class instructor email address
STATUS:TENTATIVE                            Event status
LAST-MODIFIED:20050514T104000               Date/time of last modification
X-R25-TYPE:Section                          R25 event type
X-R25-ORGANIZATION:ACCOUNTING               Department name
X-R25-HEADCOUNT;X-R25-TYPE=EXPECTED:50      Expected head count
DESCRIPTION                                 Descriptive text
LOCATION                                    Position
CATEGORIES                                  
DTSTART:20050917T090000                     Start and end date/times of the first class occurrence
DTEND:20050917T103000                       Start and end date/times of the first class occurrence
RRULE:W1 TU TH 20051212T235900              Recurring date/time pattern of the class
X-R25-PREFERENCE;X-R25-TYPE=SPACE;          X-R25 custom property, parameter, and value that define the space preference of the class
X-R25-SUBTYPE=SPACE:BCC101                  X-R25 custom property, parameter, and value that define the space preference of the class
END:VEVENT                                  End of vEvent object
END:VCALENDAR                               End of vCalendar object
"""