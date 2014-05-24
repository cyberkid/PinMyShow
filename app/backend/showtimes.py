from flask_restful import Resource
from flask import request
import requests

from BeautifulSoup import BeautifulSoup
import re

from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging
import logging

client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)


class Showtimes(Resource):
    def get(self,movie):
        url="http://www.google.com/movies?near=bangalore&q="+movie;
        resp=requests.get(url)
        content=re.findall(r"\<div\>.*\<\/div\>",resp.content)
        soup =BeautifulSoup(content[0])
        result=soup.find(id="movie_results")
        return result,200



