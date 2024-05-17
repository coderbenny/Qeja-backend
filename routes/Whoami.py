from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from lib import User

class Whoami(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        
        return jsonify({
                    "id":user.id,
                    "name":user.name,
                    "email":user.email,
                    "role_id":user.role_id, 
                    "profile":user.profile.to_dict(),
                    "followers":user.follower_count,
                    "following":user.following_count
                })