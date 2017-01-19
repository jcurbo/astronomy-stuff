import ephem
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astroplan

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

atime = Time(date_start)
loc = EarthLocation(lat=my_lat, lon=my_lon)

for x in range(0,365):
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

    print("    Moonrise: {0}".format(ephem.localtime(moonrise)))
    print("    Moonset:  {0}".format(ephem.localtime(moonset)))

    obs.date = obs.date + 1



