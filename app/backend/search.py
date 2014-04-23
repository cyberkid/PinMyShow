from flask import Flask, request
from flask.ext import restful
import requests

class Search(restful.Resource):
    def get(self,search_string): 
        movies = requests.get('http://yts.re/api/list.json?keywords='+ search_string )
        response = movies.json()
        try:
            if response['status']=='fail': 
                imdb = requests.get('http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q='+ search_string)
                return imdb.json(),310
        except:
            pass
        return response,200
