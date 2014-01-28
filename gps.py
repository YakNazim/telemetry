DATA = False

def init_constellation():
    try:
        with open('data/gps.tle') as tles:
            print tles.read()
    except:
        print "WARNING: GPS tle failed to load"
        DATA = False

