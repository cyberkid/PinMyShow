import base64
from hashlib import sha256
import os
import logging
import datetime

from flask import request
from flask_restful import Resource
from pymongo import MongoClient

from config import Config
from actions import auth_token_matches
from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging


client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)


class RegisterUser(Resource):
    def post(self):
        request_params = request.get_json()
        #try:
        #    email_id = request_params['email']
        #    auth_token = request_params['auth_token']
        #    gcm_id = request_params['gcm_id']
        #except KeyError:
        #    return {'status': 401, 'message': 'Access Unauthorized'}, 401
        #except TypeError:
        #    return {'status': 400, 'message': 'Bad Request'}, 400

        #if email_id == None or auth_token == None:
        #    return {'status': 401, 'message': 'Access Unauthorized'}, 401
        #elif auth_token_matches(email_id, gcm_id, auth_token) == False:
        #    return {'status': 401, 'message': 'Access Unauthorized'}, 401

        client = MongoClient()
        http_code = 201
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]
        auth_token = request_params['auth_token']
        logger.warning("Register/Update user: %s, auth_token: %s", request_params['email'], auth_token)
        request_params['_id'] = sha256(request_params['email']).hexdigest()
        check = collection.find({'email': request_params['email']})
        access_token = base64.urlsafe_b64encode(os.urandom(30))
        status = {'status': 201, 'message': 'Successfully Created', 'access_token': access_token}
        request_params['access_token'] = access_token
        if check.count() > 0:
            status = {'status': 200, 'message': 'Successfully Updated', 'access_token': access_token}
            http_code = 200
            collection.update({'email': request_params['email']}, {"$set": request_params}, upsert=False)
        else:
            request_params['join_date'] = datetime.datetime.utcnow()
            create_id = collection.save(request_params)
        return status, http_code

