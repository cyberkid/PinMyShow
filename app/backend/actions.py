from pymongo import MongoClient
from config import Config
from gcm import GCM
import hashlib
import time

from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging
import logging

client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)

gcm=GCM(Config.API_KEY_GCM)

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

def emailFromAccessToken(access_token):
    client=MongoClient()
    db=client[Config.DB_PMS]
    collection=db[Config.COLLECTION_USERS]
    result=collection.find_one({'access_token':access_token})
    if result == None:
        return None
    else:
        return result['email']

def access_token_validation(access_token):
    client=MongoClient()
    db=client[Config.DB_PMS]
    collection=db[Config.COLLECTION_USERS]
    result=collection.find_one({'access_token':access_token})
    if result == None:
        return False
    else:
        return True

def ts_signature_validation(timestamp,signature):
    ts=str(timestamp)
    salt="sig"+ts[::-1]+"nature"
    m=hashlib.md5()
    m.update(salt)
    sysTs = int(time.time())*1000L
    if m.hexdigest() in signature:
        if sysTs >= timestamp >= sysTs-180000L:
            return True
        else:
            return False
    else:
        return False

def auth_token_matches(email_id,gcm_id,auth_token):
    salt =gcm_id[0:6]+email_id[::-1]
    m=hashlib.md5()
    m.update(salt)
    if m.hexdigest() in auth_token:
        return True
    else:
        return False

def sendNotification(gcm_id,message):
    data = {'message': message}
    try:
        gcm.plaintext_request(registration_id=gcm_id, data=data)
    except Exception as e:
        logger.error("GCM push failed "+e.message)
        return "Failed"
    return "Success"

def sendNotificationToUser(email,data):
    client=MongoClient()
    db=client[Config.DB_PMS]
    collection=db[Config.COLLECTION_USERS]
    result=collection.find_one({'email':email})

    if result==None:
        logger.error("sendNotificationToUser Error: no email found %s",email)
        return "Failed"

    gcm_id=result['gcm_id']
    if gcm_id == None:
        logger.error("sendNotificationToUser Error: no gcm_id found for %s",email)
        return "Failed"

    data = data
    try:
        gcm.plaintext_request(registration_id=gcm_id, data=data)
    except Exception as e:
        logger.error("sendNotificationToUser failed "+e.message)
        return "Failed"
    return "Success"








