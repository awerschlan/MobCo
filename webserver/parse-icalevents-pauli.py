#!/usr/bin/env python3

import icalevents
import icalparser
from datetime import datetime, date, time
from dateutil.parser import parse
from pytz import timezone
from cairosvg import svg2png
import re
import sys

debug = True
tz = timezone("Europe/Vienna")

if len(sys.argv) < 2 :
    print("Error: location has to be set as argument")
    sys.exit (1)
else:
    location = sys.argv[1]

# Test
start = tz.localize(datetime(2018, 6, 3, 9, 30 , 0))
end = tz.localize(datetime(2018, 6, 3, 23, 59 , 59))
# Production
#start = tz.localize(datetime.now())
#end = tz.localize(datetime.combine(date.today(), time(23, 59, 59)))

# create list of icalevents objects from ics file
events_unsorted = icalevents.events('https://zimbra.visotech.com/home/' + location + '/calendar?fmt=ics&start=0day&end=7day', start=start, end=end)
# sort events using lambda function (functional programming)
events = sorted(events_unsorted, key=lambda event: event.start, reverse=False)
# delete all list elements starting from index 2
del events[2:]

# if there are no events in the ics file, then room = free for the whole day
if len(events) == 0:
    # create new "free" event object
    event = icalparser.Event()
    event.summary = 'Frei'
    event.organizer = ''
    event.start = 'bis '
    event.end = (datetime.combine(date.today(), time(20, 00, 00)))
    # append free event to list
    events.append(event)

# if start time of first event > current time, then room = free until next event
elif events[0].start > start:
    # create new "free" event object
    event = icalparser.Event()
    event.summary = 'Frei'
    event.organizer = ' '
    event.start = 'bis'
    # use beginning of next event as end time for "free" event
    event.end = events[0].start
    # insert free event as new first event in list
    events.insert(0, event)
    # trim list to two events
    del events[2:]

# if there is only 1 event in list, append second (NULL) event
if len(events) == 1:
   # create new "free" event object
    event = icalparser.Event()
    event.summary = 'NULL'
    # append free event to list
    events.append(event)
    
if debug == True:
    print("\tstart: %s" %(start))
    print("\tend: %s" %(end))
    print("\n\tnumber of events: %s" %(len(events)))


# read the SVG template
with open('files/vorlage.svg', 'r') as file:
    filedata = file.read()

# convert location to human friendly format
hlocation = re.sub(r'(\d$)', r' \1' , location.title())
filedata = filedata.replace('_location', hlocation)

# write current date in iso8601 format
filedata = filedata.replace('_current_date', str(datetime.now().isoformat(timespec='seconds')))

# main loop through list of events
for event in events:
    if debug == True:
        print("\t\tEVENT:")
        if hasattr(event, 'summary'):
            print("\t\t\tEvent summary: %s" %(event.summary))
        if hasattr(event, 'description'):
            print("\t\t\tEvent description: %s" %(event.description))
        if hasattr(event, 'organizer'):
            print("\t\t\tOrganizer: %s" %(event.organizer))
        print("\t\t\tEvent datestart : %s" %(event.start))
        print("\t\t\tEvent dateend : %s" %(event.end))

    # free events need to be handled differently (text instead of date object in event.start and/or event.end)   
    if event.summary == 'Frei':
        filedata = filedata.replace('_summary_' + str(events.index(event)), str(event.summary))
        filedata = filedata.replace('_organizer_' + str(events.index(event)), str(event.organizer))
        filedata = filedata.replace('_start_' + str(events.index(event)), str(event.start))
        filedata = filedata.replace('_end_' + str(events.index(event)), event.end.strftime('%H:%M'))

    # NULL events delete all event data in template
    elif event.summary == 'NULL':
        filedata = filedata.replace('_summary_' + str(events.index(event)), ' ')
        filedata = filedata.replace('_organizer_' + str(events.index(event)), ' ')
        filedata = filedata.replace('_start_' + str(events.index(event)), ' ')
        filedata = filedata.replace('_end_' + str(events.index(event)), ' ')

    # real events replace event placeholders in SVG template
    else:
        filedata = filedata.replace('_summary_' + str(events.index(event)), str(event.summary))
        filedata = filedata.replace('_organizer_' + str(events.index(event)), str(event.organizer))
        filedata = filedata.replace('_start_' + str(events.index(event)), event.start.strftime('%H:%M'))
        filedata = filedata.replace('_end_' + str(events.index(event)), event.end.strftime('%H:%M'))

# Write the file out again
with open('files/' + location + '.svg', 'w') as file:
    file.write(filedata) 

# Convert SVG in filedata and write to PNG File
svg2png(bytestring=filedata, write_to='files/' + location + '.png')
# PNG File -> Directory for PHP Script
svg2png(bytestring=filedata, write_to='contents/static_image/' + location + '.png')