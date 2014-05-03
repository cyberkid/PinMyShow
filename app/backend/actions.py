from pymongo import MongoClient
from config import Config


def store_movies(mid, movies, collection_name):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[collection_name]
    for movie in movies:
        #movie['_id'] = movie[mid]
        collection.save(movie)
