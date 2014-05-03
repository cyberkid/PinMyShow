
from flask import request
from flask_restful import Resource
import base64
from pymongo import MongoClient
from config import Config
from hashlib import sha256, sha1
import datetime

class RegisterUser(Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        status =  {'status_code':201, 'message': 'Successfully Created'}
        http_code = 201
        db = client[Config.DB_PMS]
        collection = db['users']
        status['token'] = base64.b64encode(sha1(request_params['email']).hexdigest())
        request_params['_id'] = sha256(request_params['email']).hexdigest()
        check = collection.find_one({'email':request_params['email']})
        if check.count() > 0:
            try:
                request_params['pins'] = check['pins']
            except KeyError:
                pass
            status = {'status_code':200, 'message': 'Successfully Updated'}
            http_code = 200
        else:
            request_params['join_date'] = datetime.datetime.utcnow()
        create_id = collection.save(request_params)
        return status, http_code

