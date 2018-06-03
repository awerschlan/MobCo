#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import icalendar
import urllib.request
import base64

#url = 'https://zimbra.visotech.com/home/besprechungsraum4/calendar?fmt=ics&start=0day&end=4day'
url = 'https://zimbra.visotech.com/home/besprechungsraum4/calendar'
base64string = 'ZG9vcnNpZ246cm9vZG5naXM='

request = urllib.request.Request(url)
request.add_header("Authorization", "Basic %s" % base64string)   
response = urllib.request.urlopen(request)
data = response.read()

ical = icalendar.Calendar.from_ical(data)

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