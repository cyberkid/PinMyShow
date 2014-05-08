from flask import request
from flask_restful import Resource

from rt import rt_search, rt_boxoffice, rt_upcoming
from trakt import trakt_get_data
from omdb import omdb_get_data
from actions import store_movies, store_one_movie
from config import Config


def get_detailed_movies(movies):
    rt_imgage_default = "http://images.rottentomatoescdn.com/images/redesign/poster_default.gif"
    pms_image_default = "http://54.187.114.0/poster_default.jpeg"

    response = []
    for movie in movies:
        item = {}
        tmp = {}
        try:
            assert movie['alternate_ids']['imdb']
            try:
                item['rt_id'] = movie['id']
                item['imdb_id'] = movie['alternate_ids']['imdb']
                tmp['omdb'] = omdb_get_data(movie['alternate_ids']['imdb'])
            except Exception, e:
                print 'OMDB lookup error'
            try:
                tmp['trakt'] = trakt_get_data(movie['alternate_ids']['imdb'])
            except Exception:
                pass
            try:
                item['mpaa_rating'] = movie['mpaa_rating']
            except KeyError:
                pass
            try:
                item['title'] = movie['title']
            except KeyError:
                pass
            try:
                if movie['runtime']:
                    item['runtime'] = movie['runtime']
                else:
                    item['runtime'] = tmp['trakt']['runtime']
            except KeyError:
                pass
            try:
                item['rating'] = "{0:.2f}".format(
                    movie['ratings']['critics_score'] *
                    0.05)
            except:
                pass
            try:
                item['images'] = {}
                if rt_imgage_default in movie['posters']['thumbnail']:
                    item['images']['thumbnail'] = pms_image_default
                else:
                    item['images']['thumbnail'] = movie['posters']['thumbnail']

                if rt_imgage_default in movie['posters']['detailed']:
                    item['images']['medium'] = pms_image_default
                else:
                    item['images']['medium'] = movie['posters']['detailed']

                if rt_imgage_default in movie['posters']['original']:
                    item['images']['original'] = pms_image_default
                else:
                    item['images']['original'] = movie['posters']['original']


                item['images']['poster'] = tmp['omdb']['Poster']
                item['images']['fanart'] = tmp['trakt']['images']['fanart']
            except KeyError:
                pass

            if item['images']['thumbnail'] == None:
                 item['images']['fanart'] = pms_image_default

            if item['images']['poster'] == None:
                   item['images']['poster'] = pms_image_default
            try:
                item['release_dates'] = {}
                item['release_dates']['theater'] = movie[
                    'release_dates']['theater']
            except:
                pass
            try:
                item['release_dates']['theater'] = movie[
                    'release_dates']['dvd']
            except:
                pass
            try:
                item['cast'] = tmp['omdb']['Actors']
            except KeyError:
                pass
            try:
                if tmp['trakt']['overview']:
                    item['summary'] = tmp['trakt']['overview']
                elif tmp['omdb']['Plot']:
                    item['summary'] = tmp['omdb']['Plot']
                elif movie['synopsis']:
                    item['summary'] = movie['synopsis']
            except KeyError:
                pass
            try:
                item['languages'] = tmp['omdb']['Language']
            except KeyError:
                pass
            try:
                item['country'] = tmp['omdb']['Country']
            except KeyError:
                pass
            try:
                item['storyboard'] = tmp['omdb']['Writer']
            except KeyError:
                pass
            try:
                item['director'] = tmp['omdb']['Director']
            except KeyError:
                pass
            try:
                item['genre'] = tmp['omdb']['Genre']
            except KeyError:
                pass
            try:
                item['awards'] = tmp['omdb']['Awards']
            except KeyError:
                pass
            try:
                if tmp['trakt']['tagline']:
                    item['tagline'] = tmp['trakt']['tagline']
            except KeyError:
                pass
            try:
                item['people'] = tmp['trakt']['people']
            except KeyError:
                pass
            try:
                item['trailer'] = tmp['trakt']['trailer']
            except KeyError:
                pass
            response.append(item)
            store_one_movie(item['rt_id'], item, Config.COLLECTION_MOVIES)
        except KeyError:
            print 'No IMDB id'
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
            store_movies('id', search_result['movies'], Config.COLLECTION_RT)
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

