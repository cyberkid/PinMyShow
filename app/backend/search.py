from flask import request
from flask_restful import Resource

from rt import rt_search, rt_boxoffice, rt_upcoming
from trakt import trakt_get_data
from omdb import omdb_get_data
from actions import store_movies
from config import Config


def get_detailed_movies(movies):
    response = []
    for movie in movies:
        item = {}
        tmp = {}
        try:
            item['rt_id'] = movie['id']
            item['imdb_id'] = movie['alternate_ids']['imdb']
            tmp['omdb'] = omdb_get_data(movie['alternate_ids']['imdb'])
        except Exception, e:
            #failed_omdb = open("/home/ubuntu/failed_omdb", "a")
            #failed_omdb.write(str(e) + "\n")
            #failed_omdb.close()
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
            item['images']['thumbnail'] = movie['posters']['thumbnail']
            item['images']['medium'] = movie['posters']['detailed']
            item['images']['original'] = movie['posters']['original']
            item['images']['poster'] = tmp['omdb']['Poster']
            item['images']['fanart'] = tmp['trakt']['images']['fanart']
        except KeyError:
            pass
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

