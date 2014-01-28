import re
import os
import ephem
import datetime

DATA = False
TLE_FILE = os.path.join(os.path.dirname(__file__), 'data/gps.tle')
SITE = ephem.Observer()
SITE.lon, SITE.lat = '-122.631007', '45.51200'

prn = re.compile('\PRN [0-9]*')


def init_constellation():
    sats = {}
    try:
        with open(TLE_FILE, 'r') as tles:
            PRN = ""
            for line in tles:
                if len(line) < 70:
                    PRN = int(prn.search(line).group(0)[-2:])
                else:
                    if PRN not in sats:
                        sats[PRN] = {'lines': []}
                    sats[PRN]['lines'].append(line)
    except:
        print "WARNING: GPS tle failed to load"
        DATA = False
        return

    for PRN, sat in sats.iteritems():
        name = "%02d" % PRN
        e = ephem.readtle(name, sat['lines'][0], sat['lines'][1])
        sat['ephem'] = e

    DATA = True
    return sats

def compute(sats):
    now = ephem.now()
    SITE.date = now

    count = 0
    sky = []
    for PRN, sat in sats.iteritems():
        sat['ephem'].compute(SITE)
        if sat['ephem'].alt > 0:
            count += 1
            sky.append({'prn': PRN, 'alt': sat['ephem'].alt, 'az': sat['ephem'].az})
            

    return {'Num_Sats': count, 'Sky': sky}
