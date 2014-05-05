
from flask import request
from flask_restful import Resource

from config import Config
from pymongo import MongoClient

from rt import rt_movie_info

from search import get_detailed_movies
import json
from hashlib import sha256
import datetime

class PinMovie(Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]
        user = collection.find_one({'email':request_params['email']})
        try:
            if request_params['rt_id']:
                for rt_id in request_params['rt_id']:
                    if rt_id not in user['pins']:
                        user['pins'].append(str(rt_id))
        except KeyError:
            user['pins'] = []
            if request_params['is_list'] == 'True':
                user['pins'] += request_params['rt_id']
            else:
                user['pins'].append(request_params['rt_id'])
        create_id = collection.save(user)
        return 'Saved'


class UnPin(Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]
        user = collection.find_one({'email':request_params['email']})
        try:
            if request_params['is_list'] == 'True':
                user['pins'] += request_params['rt_ids']
            elif request_params['rt_id'] not in user['pins']:
                user['pins'].append(request_params['rt_id'])
        except KeyError:
            user['pins'] = []
            if request_params['is_list'] == 'True':
                user['pins'] += request_params['rt_id']
            else:
                user['pins'].append(request_params['rt_id'])
        create_id = collection.save(user)
        return 'Removed'


class MyPins(Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]
        user = collection.find_one({'email':request_params['email']})
        mylist = []
        for pin in user['pins']:
            mylist.append(rt_movie_info(pin))
        mypins = get_detailed_movies(mylist)
        return mypins