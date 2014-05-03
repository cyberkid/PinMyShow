import requests

from pymongo import MongoClient
from config import Config
import json
from actions import store_one_movie


def online_lookup(imdb_id):
    if 'tt' in imdb_id:
        url = 'http://www.omdbapi.com/?i=' + imdb_id
    else:
        url = 'http://www.omdbapi.com/?i=tt' + imdb_id
    omdb = json.loads(requests.get(url).content)
    store_one_movie('imdbID', omdb, Config.COLLECTION_OMDB)
    return omdb


def db_lookup(imdb_id):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[Config.COLLECTION_OMDB]
    return collection.find_one({'imdbID': 'tt' + imdb_id})


def omdb_get_data(imdb_id):
    db_result = db_lookup(imdb_id)
    if db_result:
        return db_result
    else:
        return online_lookup(imdb_id)






