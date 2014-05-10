from pymongo import MongoClient
from config import Config


def store_movies(mid, movies, collection_name):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[collection_name]
    for movie in movies:
        movie['_id'] = movie[mid]
        collection.save(movie)


def store_one_movie(mid, movie, collection_name):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[collection_name]
    movie['_id'] = movie[mid]
    collection.save(movie)


def db_lookup_movies(rt_id):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[Config.COLLECTION_MOVIES]
    return collection.find_one({'_id': rt_id})

def access_token_matches(email_id,access_token):
    client=MongoClient()
    db=client[Config.DB_PMS]
    collection=db[Config.COLLECTION_USERS]
    result=collection.find_one({'email':email_id})
    if result == None:
        return False
    elif result['access_token'] in access_token:
        return True
    else:
        return False




