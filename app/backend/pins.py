from flask import request
from flask_restful import Resource

from config import Config
from pymongo import MongoClient

from rt import rt_movie_info
from actions import db_lookup_movies, access_token_validation,emailFromAccessToken

from search import get_detailed_movies

from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging
import logging

client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)

class PinMovie(Resource):
    def post(self):
        request_params = request.get_json()
        try:
            access_token = request_params['access_token']
        except KeyError:
            return {'status': 400, 'message': 'Bad Request'}, 400
        except TypeError:
            return {'status': 401, 'message': 'Access Unauthorized'}, 401

        if access_token == None:
            return {'status': 400, 'message': 'Bad Request'}, 400
        elif access_token_validation(access_token) == False:
            return {'status': 401, 'message': 'Access Unauthorized'}, 401

        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]

        email=emailFromAccessToken(access_token)
        if email == None:
            logger.error("PinMovies email not found for access_token='"+access_token+"'")
            return {'status': 501, 'message': 'Email not found for access token'}, 501

        user = collection.find_one({'email': email})

        try:
            if request_params['rt_id']:
                for rt_id in request_params['rt_id']:
                    if rt_id not in user['pins']:
                        user['pins'].append(str(rt_id))
        except KeyError:
            user['pins'] = []
            for rt_id in request_params['rt_id']:
                if rt_id not in user['pins']:
                    user['pins'].append(str(rt_id))
        create_id = collection.save(user)
        status = {'status': 201, 'message': 'Successfully Pinned'}
        return status, 201


class UnPin(Resource):
    def post(self):
        request_params = request.get_json()
        try:
            access_token = request_params['access_token']
        except KeyError:
            return {'status': 400, 'message': 'Bad Request'}, 400
        except TypeError:
            return {'status': 400, 'message': 'Bad Request'}, 400

        if access_token == None:
            return {'status': 400, 'message': 'Bad Request'}, 400
        elif access_token_validation(access_token) == False:
            return {'status': 401, 'message': 'Access Unauthorized'}, 401

        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]

        email=emailFromAccessToken(access_token)
        if email == None:
            logger.error("PinMovies email not found for access_token='"+access_token+"'")
            return {'status': 501, 'message': 'Email not found for access token'}, 501

        user = collection.find_one({'email': email})

        try:
            if request_params['rt_id']:
                for rt_id in request_params['rt_id']:
                    try:
                        user['pins'].remove(str(rt_id))
                    except ValueError:
                        pass
        except KeyError:
            return {'status': 400, 'message': 'Bad Request'}, 400
        except TypeError:
            return {'status': 400, 'message': 'Bad Request'}, 400

        create_id = collection.save(user)
        status = {'status': 200, 'message': 'Successfully UnPinned'}
        return status, 200


class MyPins(Resource):
    def post(self):
        request_params = request.get_json()
        try:
            access_token = request_params['access_token']
        except KeyError:
            return {'status': 400, 'message': 'Bad Request'}, 400
        except TypeError:
            return {'status': 400, 'message': 'Bad Request'}, 400


        if access_token == None:
            return {'status': 400, 'message': 'Bad Request'}, 400
        elif access_token_validation(access_token) == False:
            return {'status': 401, 'message': 'Access Unauthorized'}, 401

        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]

        email=emailFromAccessToken(access_token)
        if email == None:
            logger.error("PinMovies email not found for access_token='"+access_token+"'")
            return {'status': 501, 'message': 'Email not found for access token'}, 501

        user = collection.find_one({'email': email})

        mylist = []
        try:
            for pin in user['pins']:
                mylist.append(rt_movie_info(pin))
            mypins = get_detailed_movies(mylist)
            response = {}
            response['data'] = {}
            response['data']['movies'] = mypins
            response['data']['count'] = len(user['pins'])
        except KeyError:
            response = {}
            response['data'] = {}
            response['data']['movies'] = []
            response['data']['count'] = 0

        return response, 200