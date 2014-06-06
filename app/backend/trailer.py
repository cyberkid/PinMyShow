import logging

from flask_restful import Resource
import requests
from flask import request
from BeautifulSoup import BeautifulSoup

import feedparser
from actions import ts_signature_validation
from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging

client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)


class Trailers(Resource):
    def get(self, search_string):
        ts = request.args.get('ts')
        signature = request.args.get('signature')

        if ts == None or signature == None or ts_signature_validation(ts, signature) == False:
            return {'status': 401, 'message': 'Invalid signature'}, 401

        default = "/default.jpg"
        hq = "/hqdefault.jpg"
        mq = "/mqdefault.jpg"
        sd = "/sddefault.jpg"
        max = "/maxresdefault.jpg"
        #
        source_url = "http://www.youtube.com/results?search_query=" + search_string + " trailer"
        youtube_page = requests.get(source_url)
        soup = BeautifulSoup(youtube_page.content)
        k = soup.find(id="search-results")
        response = {}
        response["trailer"] = "http://www.youtube.com{0}".format(k.a.get('href'))
        thumb_path = "http:{0}".format(k.img['src']).rsplit("/", 1)[0]
        response["defaultThumb"] = thumb_path + default
        response["hqThumb"] = thumb_path + hq
        response["mqThumb"] = thumb_path + mq
        response["sdThumb"] = thumb_path + sd
        response["maxThumb"] = thumb_path + max
        return response


class Trailer(Resource):
    def get(self, search_string):
        ts = request.args.get('ts')
        signature = request.args.get('signature')

        if ts == None or signature == None or ts_signature_validation(ts, signature) == False:
            return {'status': 401, 'message': 'Invalid signature'}, 401

        default = "/default.jpg"
        hq = "/hqdefault.jpg"
        mq = "/mqdefault.jpg"
        sd = "/sddefault.jpg"
        max = "/maxresdefault.jpg"
        #
        source_url = "http://gdata.youtube.com/feeds/api/videos?q=" + search_string + "+official+trailer"
        feed = requests.get(source_url)
        data = feedparser.parse(feed.content)
        response = {}
        response['title'] = search_string
        if len(data.entries) > 0:
            try:
                feed = data.entries[0];
                response['trailer'] = feed.link.replace("&feature=youtube_gdata", "")
                thumb_path = feed.media_thumbnail[0]['url'].rsplit("/", 1)[0]
                response["defaultThumb"] = thumb_path + default
                response["hqThumb"] = thumb_path + hq
                response["mqThumb"] = thumb_path + mq
                response["sdThumb"] = thumb_path + sd
                response["maxThumb"] = thumb_path + max
            except Exception as e:
                logger.error(e)
                pass
        return response, 200
