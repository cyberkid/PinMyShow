from flask import Flask, request
from flask.ext import restful
from backend.register import RegisterUser
from backend.search import Search
from backend.search import BoxOffice
from backend.search import Upcoming
from backend.trailer import Trailers
from backend.pins import PinMovie
from backend.pins import MyPins

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
api = restful.Api(app)

api.add_resource(RegisterUser, '/users/')
api.add_resource(Search, '/search/<string:search_string>/')
api.add_resource(Trailers, '/trailers/<string:search_string>/')
api.add_resource(Upcoming, '/upcoming/')
api.add_resource(BoxOffice, '/boxoffice/')
api.add_resource(PinMovie, '/pin/')
api.add_resource(MyPins, '/mypins/<string:email_id>/')

if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug= True)
