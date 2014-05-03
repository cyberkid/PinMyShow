
from flask import request
from flask.ext import restful

from actions import store_movies

import json
import requests


def get_movies(movies):
    response = []
    for movie in movies:
        try:
            item = {}
            item['id'] = movie['id']
            item['mpaa_rating'] = movie['mpaa_rating']
            item['title'] = movie['title']
	    if movie['runtime'] !="":
            	item['runtime'] = movie['runtime']
            try:
                item['rating'] = "{0:.2f}".format(
                    movie['ratings']['critics_score'] *
                    0.05)
            except:
                pass
            item['images'] = {}
            item['images']['thumbnail'] = movie['posters']['thumbnail']
            item['images']['medium'] = movie['posters']['detailed']
            item['images']['original'] = movie['posters']['original']
            item['release_dates'] = {}
            try:
                item['release_dates']['theater'] = movie[
                    'release_dates']['theater']
            except:
                pass
            try:
                item['release_dates']['theater'] = movie[
                    'release_dates']['dvd']
            except:
                pass
            item['cast'] = movie['abridged_cast']
            try:
                item['imdb_id'] = movie['alternate_ids']['imdb']
            except:
                pass
            item['summary'] = movie['synopsis']
            #trakt = requests.get('http://api.trakt.tv/movie/summary.json/480987b3b15aa0153e6d629f22a5a369/tt'+item['imdb_id']).json()
            #item['trakt']=trakt
            response.append(item)            
        except KeyError:
            print 'Some problem with rotten tomatoes'
    store_movies(response)
    return response


class Search(restful.Resource):

    def get(self, search_string):
        try:
            API_KEY = 'tj5e9gcgdp6vdbczkstww55v'
            limit = request.args.get('limit')
            page = request.args.get('page')
            search_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?page_limit={0}&page={1}&apikey={2}&q={3}".format(
                limit,
                page,
                API_KEY,
                search_string)
            search_result = json.loads(requests.get(search_url).content)
            response = {}
            response['data'] = {}
            response['data']['count'] = search_result['total']
            response['data']['movies'] = get_movies(search_result['movies'])
            return response
        except Exception as e:
            return 'Error in Search : ' + str(e), 500


class BoxOffice(restful.Resource):

    def get(self):
        try:
            API_KEY = 'tj5e9gcgdp6vdbczkstww55v'
            limit = request.args.get('limit')
            search_url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/box_office.json?limit={0}&country=in&apikey={1}".format(
                limit,
                API_KEY)
            search_result = json.loads(requests.get(search_url).content)
            response = {}
            response['data'] = {}
            movies = get_movies(search_result['movies'])
            response['data']['movies'] = movies
            response['data']['count'] = len(movies)
            return response
        except Exception as e:
            return 'Error in BoxOffice : ' + str(e), 500


class Upcoming(restful.Resource):

    def get(self):
        try:
            API_KEY = 'tj5e9gcgdp6vdbczkstww55v'
            limit = request.args.get('limit')
            page = request.args.get('page')
            search_url = "http://api.rottentomatoes.com/api/public/v1.0/lists/movies/upcoming.json?page_limit={0}&page={1}&country=in&apikey={2}".format(
                limit,
                page,
                API_KEY)
            search_result = json.loads(requests.get(search_url).content)
            response = {}
            response['data'] = {}
            response['data']['count'] = search_result['total']
            response['data']['movies'] = get_movies(search_result['movies'])
            return response
        except Exception as e:
            return 'Error in UpComing : ' + str(e), 500
