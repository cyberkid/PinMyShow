from flask import request
from flask_restful import Resource

from rt import rt_search, rt_boxoffice, rt_upcoming
from trakt import trakt_get_data
from omdb import omdb_get_data
from actions import store_movies
from config import Config

import json
import requests
from app.app import app

def get_detailed_movies(movies):
    store_movies(movies, Config.COLLECTION_RT)
    response = []
    for movie in movies:
        try:
            app.logger.error('asdasdasdasd')
            item = {}
            item['id'] = movie['id']
            item['mpaa_rating'] = movie['mpaa_rating']
            item['title'] = movie['title']
            if movie['runtime'] != "":
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
                #item['trakt_data'] = trakt_get_data(movie['alternate_ids']['imdb'])
                #item['omdb_data'] = omdb_get_data(movie['alternate_ids']['imdb'])
            except Exception as e:
                return str(e)
            item['summary'] = movie['synopsis']
            response.append(item)
        except KeyError:
            print 'Some problem with rotten tomatoes'

    return response


class Search(Resource):
    def get(self, search_string):
        try:
            limit = request.args.get('limit')
            page = request.args.get('page')
            search_result = rt_search(search_string, limit, page)
            response = {}
            response['data'] = {}
            response['data']['count'] = search_result['total']
            response['data']['movies'] = get_detailed_movies(search_result['movies'])
            return response
        except Exception as e:
            return 'Error in Search : ' + str(e), 500


class BoxOffice(Resource):
    def get(self):
        try:

            limit = request.args.get('limit')
            search_result = rt_boxoffice(limit)
            response = {}
            response['data'] = {}
            movies = get_detailed_movies(search_result['movies'])
            response['data']['movies'] = movies
            response['data']['count'] = len(movies)
            return response
        except Exception as e:
            return 'Error in BoxOffice : ' + str(e), 500


class Upcoming(Resource):
    def get(self):
        try:
            limit = request.args.get('limit')
            page = request.args.get('page')
            search_result = rt_upcoming(limit, page)
            response = {}
            response['data'] = {}
            response['data']['count'] = search_result['total']
            response['data']['movies'] = get_detailed_movies(search_result['movies'])
            return response
        except Exception as e:
            return 'Error in UpComing : ' + str(e), 500
