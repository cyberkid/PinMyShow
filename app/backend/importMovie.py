from omdb import *
from trakt import *
import sys

def import_movie(start, offset):
    for x in range(int(start), int(start)+int(offset)):
        print "start=", start, "end=", int(start)+int(offset)
        zeroes = 7 - len(str(x))
        extra=""
        for i in range(0, zeroes):
            extra += "0"
        imdb_id = "tt"+extra+str(x)
        print imdb_id
        try:
            omdb = omdb_get_data(imdb_id)
        except:
            pass
        try:
            trakt = trakt_get_data(imdb_id)
        except:
            pass
        file=open("imported",'w')
        file.write(imdb_id)
        print omdb, "\n", trakt

import_movie(sys.argv[1], sys.argv[2])
