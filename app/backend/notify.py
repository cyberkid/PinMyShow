from flask import Flask, request
from flask.ext import restful
from pymongo import MongoClient

class Notify(restful.Resource):
    def post(self): 
        request_params = request.get_json()
        client = MongoClient()
        db = client['test_pinmyshow']
        collection = db['pins']
        create_id = collection.save(request_params)
        return {'status_code':200, 'message':'Consider it done Boss!'},200
