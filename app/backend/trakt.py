import json
import random

import requests
from pymongo import MongoClient

from config import Config
from actions import store_one_movie


def trakt_create_user(email_id, retry):
    url = 'http://api.trakt.tv/account/create/' + Config.API_KEY_TRAKT
    if retry:
        username = email_id.split("@")[0] + random.randint(1111, 9999)
    else:
        username = email_id.split("@")[0]
    password = trakt_get_sha1_passwd(email_id)
    payload = {'username': username, 'password': password, 'email': email_id}
    resp = requests.post(url, data=json.dumps(payload)).json()
    if resp['status'] == 'success':
        return True, username, password
    else:
        return False, username, password


def online_lookup(imdb_id):
    if 'tt' in imdb_id:
        url = 'http://api.trakt.tv/movie/summary.json/' + Config.API_KEY_TRAKT + imdb_id
    else:
        url = 'http://api.trakt.tv/movie/summary.json/' + Config.API_KEY_TRAKT + imdb_id
    trakt = json.loads(requests.get(url).content)
    if trakt['imdb_id']:
        store_one_movie('imdb_id', trakt, Config.COLLECTION_TRAKT)
        return trakt
    raise Exception


def db_lookup(imdb_id):
    client = MongoClient()
    db = client[Config.DB_MOVIES]
    collection = db[Config.COLLECTION_TRAKT]
    return collection.find_one({'imdb_id': 'tt' + imdb_id})


def trakt_get_data(imdb_id):
    try:
        db_result = db_lookup(imdb_id)
        if db_result:
            return db_result
        return online_lookup(imdb_id)
    except Exception:
        failed_trakt = open("failed_trakt", "a")
        failed_trakt.write(imdb_id + "\n")
        failed_trakt.close()
        print 'TRAKT lookup error'


def trakt_get_sha1_passwd(email_id):
    passwd = hashlib.sha1('email_id' + Config.SALT_TRAKT).hexdigest()
    return passwd







