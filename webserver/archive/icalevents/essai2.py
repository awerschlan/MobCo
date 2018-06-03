from icalevents import icalevents
import os
import datetime
from pytz import timezone

directory = os.path.dirname(__file__)
with open(os.path.join(directory, 'MyCal1.ics'), 'rb') as fp:
    data = fp.read()

EventsFile=os.path.join(directory, 'MyCal1.ics')
tz = timezone("Europe/Brussels")
start = tz.localize(datetime.datetime(2018, 3, 20, 8, 59 , 0))
end = tz.localize(datetime.datetime(2018, 3, 30, 9, 1, 0))

evs = icalevents.events(file=EventsFile, start=start, end=end)


print("\nSearch for events within a period")
print("\tSearch period start: %s" %(start))
print("\tSearch period start timezone: %s" %(start.tzinfo))
print("\tSearch period end: %s" %(end))
print("\tSearch period end timezone: %s" %(end.tzinfo))
print("\n\tNumber of events found: %s" %(len(evs)))

for MyEvent in evs:
    print("\t\tEVENT:")
    if hasattr(MyEvent, 'summary'):
        print("\t\t\tEvent summary: %s" %(MyEvent.summary))
    if hasattr(MyEvent, 'description'):
        print("\t\t\tEvent description: %s" %(MyEvent.description))
    print("\t\t\tEvent datestart : %s" %(MyEvent.start))
    print("\t\t\tEvent datestart tzinfo: %s" %(MyEvent.start.tzinfo))
    print("\t\t\tEvent dateend : %s" %(MyEvent.end))
    print("\t\t\tEvent dateend tzinfo: %s" %(MyEvent.end.tzinfo))
