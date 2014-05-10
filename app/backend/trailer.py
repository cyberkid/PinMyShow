from flask_restful import Resource

import requests
from flask import request
from actions import access_token_matches
from BeautifulSoup import BeautifulSoup


class Trailers(Resource):
    def get(self, search_string):
        email_id=request.args.get('email')
        access_token=request.args.get('access_token')

        if email_id == None or access_token ==None:
            return {'status_code':401,'message':'Access Unauthorized'},401
        elif access_token_matches(email_id,access_token) == False:
            return {'status_code':401,'message':'Access Unauthorized'},401

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
