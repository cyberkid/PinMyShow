from flask_restful import Resource
import requests


class Search(Resource):
    def get(self, search_string):
        UpcomingMovies = []
        AvailableMovies = []
        response = {}
        if search_string == 'upcoming_search':
            movies = requests.get('http://yts.re/api/upcoming.json').json()
            for movie in movies:
                entity = {}
                entity['title'] = movie['MovieTitle']
                entity['image'] = movie['MovieCover']
                entity['imdb_id'] = movie['ImdbCode']
                entity['source'] = 'yifi'
                UpcomingMovies.append(entity)
            response['data'] = UpcomingMovies
        else:
            movies = requests.get('http://yts.re/api/list.json?keywords=' + search_string).json()
            for movie in movies['MovieList']:
                entity = {}
                entity['title'] = movie['MovieTitleClean']
                entity['image'] = movie['CoverImage']
                entity['imdb_id'] = movie['ImdbCode']
                entity['release_date'] = movie['MovieYear']
                entity['rating'] = movie['MovieRating']
                entity['MID'] = movie['MovieID']
                entity['source'] = 'yifi'
                AvailableMovies.append(entity)
            response['data'] = AvailableMovies

        return response, 200
