from flask import Flask, request
from flask.ext import restful
from backend.register import RegisterUser
from backend.search import Search
from backend.notify import Notify
app = Flask(__name__)
api = restful.Api(app)

class HelloWorld(restful.Resource):
    def post(self):
        k = request.get_json()
        return {'hi': k}

api.add_resource(RegisterUser, '/users/')
api.add_resource(Search, '/search/<string:search_string>')
api.add_resource(Notify, '/pins/')

if __name__ == '__main__':
    app.run(debug= True)
