from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from lib import db, Profile

profiles_bp = Blueprint("profiles_bp", __name__)
api = Api(profiles_bp)

class ProfilesResource(Resource):
    
    # Retrieve users from the db
    def get(self, id=None):
        if not id:
            profs = Profile.query.all()
            if not profs:
                return {"error":"No profiles exist"}, 404
        
            response = make_response(
                jsonify([prof.to_dict() for prof in profs]),
                200
            )

            return response
        
        prof = Profile.query.filter_by(id=id).first()
        if not prof:
            return {"error":"Profile does not exist"}, 404
        
        response = make_response(
            jsonify(prof.to_dict()), 
            200
        )
        
        return response 
    


api.add_resource(ProfilesResource, "/profiles", "/profiles/<int:id>")