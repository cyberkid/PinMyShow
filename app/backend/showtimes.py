import re
import logging

import requests
from BeautifulSoup import BeautifulSoup

from raven.handlers.logging import SentryHandler
from raven import Client
from raven.conf import setup_logging


client = Client('https://c08e468ddcf148d3bed9966345bdb7f4:5c4227f8d4fd4b1e94d01ebe03e29883@app.getsentry.com/23855')
handler = SentryHandler(client)
setup_logging(handler)
logger = logging.getLogger(__name__)


def getShowTime(movie, latitude, longitude):
    url = "http://www.google.com/movies?near={0},{1}&q={2}".format(latitude, longitude, movie)
    resp = requests.get(url)
    content = re.findall(r"\<div\>.*\<\/div\>", resp.content)
    soup = BeautifulSoup(content[0])
    result = soup.find(id="movie_results")
    logger.info("ShowTimes : %s", result)
    response = []
    if result != None:
        theatres = result.findAll("div", {"class": "theater"})
        for x in theatres:
            theatre = {}
            theatre["name"] = x.find("div", {"class": "name"}).text
            theatre['address'] = x.find("div", {"class": "address"}).text
            theatre['time'] = x.find("div", {"class": "times"}).text.replace("&#8206;", "").split("&nbsp;")
            response.append(theatre)
    return response
