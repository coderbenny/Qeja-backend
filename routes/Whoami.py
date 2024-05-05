from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required

from lib import User

class Whoami(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        response = make_response(
            jsonify({"name":user.name,"email":user.email, "role_id":user.role_id, "user_profile":user.profile}), 
            200
        )
        
        return response