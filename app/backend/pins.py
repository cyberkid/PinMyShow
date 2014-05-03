
from flask import request
from flask_restful import Resource

from config import Config
from pymongo import MongoClient
import json
from hashlib import sha256
import datetime

class PinMovie(Resource):
    def post(self):
        request_params = request.get_json()
        client = MongoClient()
        db = client[Config.DB_PMS]
        collection = db[Config.COLLECTION_USERS]
        user_pins = collection.find_one({'email':request_params['email']})
        try:
            if request_params['id'] not in user_pins['pins']:
                user_pins['pins'].append(request_params['id'])
        except KeyError:
            user_pins['pins'] = []
            user_pins['pins'].append(request_params['id'])
        create_id = collection.save(user_pins)
        return 'Saved'


class MyPins(Resource):
    def get(self, email_id):
        return {"data": {"movies": [{"rating": "4.45", "_id": "771312513", "title": "Captain America: The Winter Soldier", "summary": "After being deemed unfit for military service, Steve Rogers volunteers for a top secret research project that turns him into Captain America, a superhero dedicated to defending America's ideals.", "release_dates": {"theater": "2014-04-04"}, "imdb_id": "1843866", "cast": [{"name": "Chris Evans", "characters": ["Captain America/Steve Rogers"], "id": "162652784"}, {"name": "Anthony Mackie", "characters": ["Sam Wilson/Falcon"], "id": "162653786"}, {"name": "Sebastian Stan", "characters": ["Bucky Barnes/Winter Soldier"], "id": "326299814"}, {"name": "Samuel L. Jackson", "characters": ["Nick Fury"], "id": "162652156"}, {"name": "Scarlett Johansson", "characters": ["Natasha Romanoff/Black Widow"], "id": "162652872"}], "mpaa_rating": "PG-13", "images": {"medium": "http://content8.flixster.com/movie/11/17/72/11177246_det.jpg", "thumbnail": "http://content8.flixster.com/movie/11/17/72/11177246_mob.jpg", "original": "http://content8.flixster.com/movie/11/17/72/11177246_ori.jpg"}, "runtime": 136, "id": "771312513"}, {"rating": "2.45", "_id": "771355185", "title": "Heaven Is for Real", "summary": "Based on the #1 New York Times best-selling book of the same name, HEAVEN IS FOR REAL brings to the screen the true story of a small-town father who must find the courage and conviction to share his son's extraordinary, life-changing experience with the world. The film stars Academy Award (R) nominee and Emmy (R) award winning actor Greg Kinnear as Todd Burpo and co-stars Kelly Reilly as Sonja Burpo, the real-life couple whose son Colton (newcomer Connor Corum) claims to have visited Heaven during a near death experience. Colton recounts the details of his amazing journey with childlike innocence and speaks matter-of-factly about things that happened before his birth ... things he couldn't possibly know. Todd and his family are then challenged to examine the meaning from this remarkable event. (c) Sony", "release_dates": {"theater": "2014-04-16"}, "imdb_id": "1929263", "cast": [{"name": "Greg Kinnear", "characters": ["Todd Burpo"], "id": "162652891"}, {"name": "Kelly Reilly", "characters": ["Sonja Burpo"], "id": "162684910"}, {"name": "Connor Corum", "characters": ["Colton Burpo"], "id": "771472939"}, {"name": "Margo Martindale", "characters": ["Nancy Rawling"], "id": "542897020"}, {"name": "Thomas Haden Church", "characters": ["Jay Wilkins"], "id": "162683650"}], "mpaa_rating": "PG", "images": {"medium": "http://content9.flixster.com/movie/11/17/47/11174759_det.jpg", "thumbnail": "http://content9.flixster.com/movie/11/17/47/11174759_mob.jpg", "original": "http://content9.flixster.com/movie/11/17/47/11174759_ori.jpg"}, "runtime": 100, "id": "771355185"}]}}
