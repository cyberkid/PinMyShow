
from flask import Flask, request
from flask.ext import restful

import requests
from BeautifulSoup import BeautifulSoup

class Trailers(restful.Resource):
    def get(self, search_string):
	default="/default.jpg"
	hq="/hqdefault.jpg"
	mq="/mqdefault.jpg"
	sd="/sddefault.jpg"
	max="/maxresdefault.jpg"
	#
        source_url = "http://www.youtube.com/results?search_query=" + search_string+" trailer"
        youtube_page = requests.get(source_url)
        soup = BeautifulSoup(youtube_page.content)
        k = soup.find(id="search-results")
	response={}
	response["trailer"]="http://www.youtube.com{0}".format(k.a.get('href'))
	thumb_path="http:{0}".format(k.img['src']).rsplit("/",1)[0]
	response["defaultThumb"]=thumb_path+default
	response["hqThumb"]=thumb_path+hq
	response["mqThumb"]=thumb_path+mq
	response["sdThumb"]=thumb_path+sd
	response["maxThumb"]=thumb_path+max
        return response
