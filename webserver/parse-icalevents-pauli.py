#!/usr/bin/env python3

import icalevents
import icalparser
from datetime import datetime, date, time
from dateutil.parser import parse
from pytz import timezone
from cairosvg import svg2png
import re
import sys
import locale
import calendar
from isoweek import Week

debug = False

tz = timezone("Europe/Vienna")
locale.setlocale(locale.LC_ALL, 'de_AT.utf8')

if len(sys.argv) < 2 :
    print("Error: location has to be set as argument")
    sys.exit (1)
else:
    location = sys.argv[1]

# Test
#start = tz.localize(datetime(2018, 6, 9, 8, 30 , 0))
#end = tz.localize(datetime(2018, 6, 9, 23, 59 , 59))
# Production
start = tz.localize(datetime.now())
end = tz.localize(datetime.combine(date.today(), time(23, 59, 59)))

# create list of icalevents objects from ics file
events_unsorted = icalevents.events('https://zimbra.visotech.com/home/' + location + '/calendar?fmt=ics&start=-1day&end=7day', start=start, end=end)
# sort events using lambda function (functional programming)
events = sorted(events_unsorted, key=lambda event: event.start, reverse=False)
# delete all list elements starting from index 4
del events[4:]

# if there are no events in the ics file, then room = free for the whole day
if len(events) == 0:
    # create new "free" event object
    event = icalparser.Event()
    event.summary = 'Frei'
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
    # trim list to four events
    del events[4:]

# if there are less than 4 events in the list, fill it with NULL events
while len(events) < 4:
   # create new "NULL" event object
    event = icalparser.Event()
    event.summary = 'NULL'
    # append NULL event to list
    events.append(event)
    
if debug == True:
    print("\tstart: %s" %(start))
    print("\tend: %s" %(end))
    print("\n\tnumber of events: %s" %(len(events)))


# read the SVG template
if events[0].summary == 'Frei':
    with open('files/vorlage-frei-pauli.svg', 'r') as file:
        filedata = file.read()
else:
    with open('files/vorlage-besprechung-pauli.svg', 'r') as file:
        filedata = file.read()

# convert location to human friendly format
hlocation = re.sub(r'(\d$)', r' \1' , location.title())
filedata = filedata.replace('_location', hlocation)

### BEGIN Calendar
# set weeknumber
filedata = filedata.replace('_weeknumber', str(datetime.now().isocalendar()[1]))
# set current month
#filedata = filedata.replace('_month_1', calendar.month_name[int(datetime.now().strftime('%m'))])

thisweek = Week.thisweek()

filedata = filedata.replace('_monday', thisweek.monday().strftime('%d'))
filedata = filedata.replace('_tuesday', thisweek.tuesday().strftime('%d'))
filedata = filedata.replace('_wednesday', thisweek.wednesday().strftime('%d'))
filedata = filedata.replace('_thursday', thisweek.thursday().strftime('%d'))
filedata = filedata.replace('_friday', thisweek.friday().strftime('%d'))

# set month at beginning of week
filedata = filedata.replace('_month_begin', calendar.month_name[int(thisweek.monday().strftime('%m'))])
# set month at end of week
filedata = filedata.replace('_month_end', calendar.month_name[int(thisweek.friday().strftime('%m'))])
### END Calendar

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


    # if summary > more than 24 charactuers, truncate to 22
    if len (event.summary) > 24:
        event.summary = (event.summary[:22] + '..')

    # free events need to be handled differently (text instead of date object in event.start and/or event.end)   
    if event.summary == 'Frei':
        filedata = filedata.replace('_summary_' + str(events.index(event)), str(event.summary))
        filedata = filedata.replace('_organizer_' + str(events.index(event)), '')
        filedata = filedata.replace('_start_' + str(events.index(event)), '')
        if event.end is not None:
            filedata = filedata.replace('_end_' + str(events.index(event)), event.end.strftime('%H:%M'))
        else:
            filedata = filedata.replace('_end_' + str(events.index(event)), 'Tagesende')

    # NULL events delete all event data in template
    elif event.summary == 'NULL':
        filedata = filedata.replace('_summary_' + str(events.index(event)), '')
        filedata = filedata.replace('_organizer_' + str(events.index(event)), '')
        filedata = filedata.replace('_start_' + str(events.index(event)), '')
        filedata = filedata.replace('_end_' + str(events.index(event)), '')

    # real events replace event placeholders in SVG template
    else:
        filedata = filedata.replace('_summary_' + str(events.index(event)), str(event.summary))
        # workaround for missing organizers (bug due to .com migration?)
        if hasattr(event, 'organizer'):
            filedata = filedata.replace('_organizer_' + str(events.index(event)), str(event.organizer))
        else:
            filedata = filedata.replace('_organizer_' + str(events.index(event)), ' ')
        filedata = filedata.replace('_start_' + str(events.index(event)), event.start.strftime('%H:%M'))
        filedata = filedata.replace('_end_' + str(events.index(event)), event.end.strftime('%H:%M'))

# Write the file out again
with open('files/' + location + '-pauli.svg', 'w') as file:
    file.write(filedata) 

# Convert SVG in filedata and write to PNG File
svg2png(bytestring=filedata, write_to='files/' + location + '-pauli.png')
# PNG File -> Directory for PHP Script
svg2png(bytestring=filedata, write_to='contents/static_image/' + location + '-pauli.png')