from flask import Flask
from flask.ext import restful
from backend.register import RegisterUser
from backend.search import Search
from backend.search import BoxOffice
from backend.search import Upcoming
from backend.trailer import Trailers,Trailer
from backend.pins import PinMovie, MyPins, UnPin
from backend.gcmclient import GCMClient
from raven.contrib.flask import Sentry


app = Flask(__name__)
api = restful.Api(app)
sentry = Sentry(app,dsn='https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')

api.add_resource(RegisterUser, '/users/')
api.add_resource(Search, '/search/<string:search_string>/')
api.add_resource(Trailers, '/trailers/<string:search_string>/')
api.add_resource(Upcoming, '/upcoming/')
api.add_resource(BoxOffice, '/boxoffice/')
api.add_resource(PinMovie, '/pin/')
api.add_resource(MyPins, '/mypins/')
api.add_resource(UnPin, '/unpin/')
api.add_resource(GCMClient, '/gcm/')
api.add_resource(Trailer, '/trailer/<string:search_string>/')

if __name__ == '__main__':
    app.run(debug=True)
