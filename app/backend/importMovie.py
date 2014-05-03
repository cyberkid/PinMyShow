from omdb import *
from trakt import *
import sys

def import_movie(start, offset):
    successfile=open("imported",'w')
    failed_omdb=open("failedOMDB",'a')
    failed_trakt=open("failedTRAKT",'a')
    print "start=", start, "end=", int(start)+int(offset)
    for x in range(int(start), int(start)+int(offset)):
        zeroes = 7 - len(str(x))
        extra=""
        for i in range(0, zeroes):
            extra += "0"
        imdb_id = "tt"+extra+str(x)
        print imdb_id
        try:
            omdb = omdb_get_data(imdb_id)
        except:
            failed_omdb.write("failed "+imdb_id+"\n")
            pass
        try:
            trakt = trakt_get_data(imdb_id)
        except:
            failed_trakt.write("failed "+imdb_id+"\n")
            pass
        successfile.truncate()
        successfile.write(imdb_id)
    successfile.close()
    failed_omdb.close()
    failed_trakt.close()

import_movie(sys.argv[1], sys.argv[2])
