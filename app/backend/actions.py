from pymongo import MongoClient


def store_movies(movies):

    client = MongoClient()
    db = client['test_pinmyshow']
    collection = db['movies']
    for movie in movies:
        movie['_id'] = movie['id']
        collection.save(movie)
