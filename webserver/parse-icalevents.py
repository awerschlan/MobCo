from icalevents import icalevents
import datetime
from pytz import timezone

tz = timezone("Europe/Vienna")
start = tz.localize(datetime.datetime(2018, 3, 20, 8, 59 , 0))
end = tz.localize(datetime.datetime(2018, 3, 30, 9, 1, 0))

evs = icalevents.events(file='calendar.ics', start=start, end=end)

print("\tstart: %s" %(start))
print("\tend: %s" %(end))
print("\n\tnumber of events: %s" %(len(evs)))

for MyEvent in evs:
    print("\t\tEVENT:")
    if hasattr(MyEvent, 'summary'):
        print("\t\t\tEvent summary: %s" %(MyEvent.summary))
    if hasattr(MyEvent, 'description'):
        print("\t\t\tEvent description: %s" %(MyEvent.description))
    if hasattr(MyEvent, 'organizer'):
        print("\t\t\tOrganizer: %s" %(MyEvent.organizer))
    print("\t\t\tEvent datestart : %s" %(MyEvent.start))
    print("\t\t\tEvent dateend : %s" %(MyEvent.end))
