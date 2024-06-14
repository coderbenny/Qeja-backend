from flask import jsonify, make_response
from flask_restful import Resource
from lib import Profile

class ProfileByID(Resource):

    def get(self, id):
        prof = Profile.query.filter_by(id=id).first()
        if not prof:
            return {"error":"Profile does not exist"}, 404
        
        response = make_response(
            jsonify(prof.to_dict()), 
            200
        )
        
        return response 