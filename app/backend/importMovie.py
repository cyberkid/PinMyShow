from omdb import *
from trakt import *
import sys


def import_movie(start, offset):
    for x in range(int(start), int(start + offset)):
        imdb_id = "tt" + str(x)
        omdb = omdb_get_data(imdb_id)
        trakt = trakt_get_data(imdb_id)
        print omdb, "\n", trakt

import_movie(sys.argv[0], sys.argv[1])
