from omdb import *
from trakt import *
import sys


def import_movie(start, offset):
    for x in range(int(start), int(start + offset)):
        zeroes = 7 - len(str(x))
        extra=""
        for i in range(0, zeroes):
            extra += "0"
        imdb_id = "tt"+extra+str(x)
        print imdb_id
        omdb = omdb_get_data(imdb_id)
        trakt = trakt_get_data(imdb_id)
        print omdb, "\n", trakt

import_movie(sys.argv[1], sys.argv[2])
