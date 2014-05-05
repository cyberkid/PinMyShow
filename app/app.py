from flask import Flask
from flask.ext import restful
from backend.register import RegisterUser
from backend.search import Search
from backend.search import BoxOffice
from backend.search import Upcoming
from backend.trailer import Trailers
from backend.pins import PinMovie, MyPins, UnPin


app = Flask(__name__)
api = restful.Api(app)

api.add_resource(RegisterUser, '/users/')
api.add_resource(Search, '/search/<string:search_string>/')
api.add_resource(Trailers, '/trailers/<string:search_string>/')
api.add_resource(Upcoming, '/upcoming/')
api.add_resource(BoxOffice, '/boxoffice/')
api.add_resource(PinMovie, '/pin/')
api.add_resource(MyPins, '/mypins/')
api.add_resource(UnPin, '/unpin/')

if __name__ == '__main__':
    app.run(debug=True)
