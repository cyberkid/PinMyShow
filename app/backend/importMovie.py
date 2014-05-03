import sys

from omdb import *
from trakt import *
import time


def import_movie(start, offset):
    successfile = open("imported", 'w')
    print "start=", start, "end=", int(start) + int(offset)-1
    for x in range(int(start), int(start) + int(offset)):
        zeroes = 7 - len(str(x))
        extra = ""
        for i in range(0, zeroes):
            extra += "0"
        imdb_id = "tt" + extra + str(x)
        print imdb_id
        try:
            omdb = omdb_get_data(imdb_id)
        except:
            pass
        try:
            trakt = trakt_get_data(imdb_id)
        except:
            pass
        successfile.seek(0)
        successfile.truncate()
        successfile.write(imdb_id)
        time.sleep(1)
    successfile.close()


import_movie(sys.argv[1], sys.argv[2])
