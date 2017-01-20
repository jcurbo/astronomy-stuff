#!/usr/bin/python3

import ephem
from astropy.coordinates import EarthLocation
from astropy.time import Time
from astroplan import moon_illumination

from icalendar import Calendar, Event
from datetime import date, time, timedelta, datetime

my_lat = '39.0209321'
my_lon = '-77.01722708'
my_elev = 122
date_start = '2017/01/01 00:00'

obs = ephem.Observer()
moon = ephem.Moon()

obs.lat = my_lat
obs.lon = my_lon
obs.elevation = my_elev
obs.date = date_start

loc = EarthLocation(lat=my_lat, lon=my_lon)

moonrise_all = []
moonset_all = []
illum_all = []

for x in range(0,365):
# for x in range(0,1):
    print("Calculation for {0}:".format(obs.date))

    moon.compute(obs)
    if (moon.alt > 0):
        print("    Moon is currently up")
        moon_up = True
        moonrise = obs.previous_rising(moon)
        moonset = obs.next_setting(moon)
    else:
        print("    Moon is currently down")
        moon_up = False
        moonrise = obs.next_rising(moon)
        moonset = obs.next_setting(moon)

    
    illum = moon_illumination(Time(moonrise.datetime()))*100

    moonrise_all.append(ephem.localtime(moonrise))
    moonset_all.append(ephem.localtime(moonset))
    illum_all.append(illum)

    print("    Moonrise: {0}".format(ephem.localtime(moonrise)))
    print("    Moonset:  {0}".format(ephem.localtime(moonset)))
    print("    Illum:    {0:.0f}%".format(illum))

    obs.date = obs.date + 1

# ical stuff starts here
cal = Calendar()
cal.add('prodid', '-//python icalendar//python.org//')
cal.add('version', '2.0')

for r, s, i in zip(moonrise_all, moonset_all, illum_all):
    # moonrise event
    e1 = Event()
    moonrise_simpletime = time.strftime(r.time(), "%H:%M")
    e1.add('uid', "{0}@curbo.org".format(r.isoformat()))
    e1.add('summary', "Moonrise at {0}, illum {1:.0f}%".format(moonrise_simpletime, i))
    e1.add('dtstart', r)
    e1.add('dtend', r + timedelta(minutes=15))
    e1.add('dtstamp', datetime.now())
    cal.add_component(e1)

    # moonset event
    e2 = Event()
    moonset_simpletime = time.strftime(s.time(), "%H:%M")
    e2.add('uid', "{0}@curbo.org".format(s.isoformat()))
    e2.add('summary', "Moonset at {0}, illum {1:.0f}%".format(moonset_simpletime, i))
    e2.add('dtstart', s)
    e2.add('dtend', s + timedelta(minutes=15))
    e2.add('dtstamp', datetime.now())
    cal.add_component(e2)

# write out the ics file
f = open('moon.ics', 'wb')
f.write(cal.to_ical())
f.close()

