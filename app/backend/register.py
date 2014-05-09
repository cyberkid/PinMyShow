
from flask import request
from flask_restful import Resource
import base64
from pymongo import MongoClient
from config import Config
from hashlib import sha256, sha1

from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging
import logging
import datetime



client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)

class RegisterUser(Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        status =  {'status_code':201, 'message': 'Successfully Created'}
        http_code = 201
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]
        auth_token=request_params['auth_token']
        logger.warning("Register/Update user: %s, auth_token: %s",request_params['email'],auth_token)
        status['token'] = base64.b64encode(sha1(request_params['email']).hexdigest())
        request_params['_id'] = sha256(request_params['email']).hexdigest()
        check = collection.find({'email':request_params['email']})
        if check.count() > 0:
            status = {'status_code':200, 'message': 'Successfully Updated'}
            http_code = 200
            collection.update({'email':request_params['email']}, {"$set": request_params }, upsert=False)
        else:
            request_params['join_date'] = datetime.datetime.utcnow()
            create_id = collection.save(request_params)
        return status, http_code

