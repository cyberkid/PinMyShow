from flask import Flask, request
from flask_restful import Resource
from pymongo import MongoClient

class Notify(Resource):
    def post(self): 
        request_params = request.get_json()
        client = MongoClient()
        db = client['test_pinmyshow']
        collection = db['pins']
        create_id = collection.save(request_params)
        return {'status':200, 'message':'Consider it done Boss!'},200
