from omdb import *
from trakt import *


def importMovie(start, offset):
    for x in range(start, start + offset):
        imdb_id = "tt" + str(x)
        omdb = omdb_get_data(imdb_id)
        trakt = trakt_get_data(imdb_id)
        print omdb, "\n", trakt
