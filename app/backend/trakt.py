import requests

import json
from pymongo import MongoClient
from config import Config
from actions import store_movies


def online_lookup(imdb_id):
    if 'tt' in imdb_id:
        url = 'http://api.trakt.tv/movie/summary.json/480987b3b15aa0153e6d629f22a5a369/' + imdb_id
    else:
        url = 'http://api.trakt.tv/movie/summary.json/480987b3b15aa0153e6d629f22a5a369/tt' + imdb_id
    trakt = json.loads(requests.get(url).content)
    store_movies('imdb_id', trakt, Config.COLLECTION_TRAKT)
    return trakt


def db_lookup(imdb_id):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[Config.COLLECTION_TRAKT]
    return collection.find_one({'imdb_id': 'tt' + imdb_id})


def trakt_get_data(imdb_id):
    db_result = db_lookup(imdb_id)
    if db_result:
        return db_result
    else:
        return online_lookup(imdb_id)










