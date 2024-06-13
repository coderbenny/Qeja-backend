from flask import jsonify, make_response
from flask_restful import Resource
from lib import Profile



class Profiles(Resource):
    
    def get(self):
        profs = Profile.query.all()
        if not profs:
            return {"error":"No profiles exist"}, 404
    
        response = make_response(
            jsonify([prof.to_dict() for prof in profs]),
            200
        )

        return response
