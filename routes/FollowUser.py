from flask_restful import Resource
from flask import request, jsonify
from lib import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

class FollowUser(Resource):
    @jwt_required()
    def post(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            user_to_follow = User.query.get(user_id)
            
            if user_to_follow is None:
                return {"message": "User not found"}, 404
            
            if current_user.is_following(user_to_follow):
                return {"message": "Already following"}, 400
            
            current_user.follow(user_to_follow)
            db.session.commit()
            return {"message": f"You are now following {user_to_follow.name}"}, 200
        except Exception as e:
            return {"message": "Internal server error"}, 500

