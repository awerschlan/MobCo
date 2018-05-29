#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import icalendar

icalfile = open('calendar.ics', 'rb')
ical = icalendar.Calendar.from_ical(icalfile.read())

for component in ical.walk():
    if component.name == "VEVENT":
        summary = component.get('summary')
        description = component.get('description')
        startdt = component.get('dtstart').dt
        enddt = component.get('dtend').dt
        exdate = component.get('exdate')

        if component.has_key('organizer'):
            organizer = component.get('organizer').params.get('CN')
        else:
            organizer = ''
        if component.has_key('location'):
            location = component.get('location')
        else:
            location = ''
 
        print ("{0} - {1} | {2}: {3} {4}".format(startdt.strftime("%H:%M"), enddt.strftime("%H:%M"), summary, organizer, location))

icalfile.close()
