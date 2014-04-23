from flask import Flask, request
from flask.ext import restful

from pymongo import MongoClient
import json
from hashlib import sha256
import datetime

class RegisterUser(restful.Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        status =  {'status_code':201, 'message': 'Successfully Created'}
        http_code = 201
        db = client['test_pinmyshow']
        collection = db['users']
        request_params['_id'] = sha256(request_params['email']).hexdigest()
        request_params['join_date'] = datetime.datetime.utcnow()
        check = collection.find({'email':request_params['email']})
        if check.count() > 0:    
            status = {'status_code':200, 'message': 'Successfully Updated'}
            http_code = 200
        create_id = collection.save(request_params)
        return status, http_code
