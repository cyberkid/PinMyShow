from flask import Flask, request
from flask.ext import restful
from pymongo import MongoClient

class BoxOffice(restful.Resource):
    def get(self):
        limit = 15
        search_url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?limit={0}&country=in&apikey=tj5e9gcgdp6vdbczkstww55v".format(limit)
        search_result = json.loads(requests.get(search_url).content)
        return {'status_code':200, 'message':'Consider it done Boss!'},200

