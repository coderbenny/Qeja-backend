from flask_restful import Resource
from flask import request, jsonify
from lib import db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

class UnfollowUser(Resource):
    @jwt_required()
    def post(self, user_id):
        try:
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            user_to_unfollow = User.query.get(user_id)
            
            if user_to_unfollow is None:
                return {"message": "User not found"}, 404
            
            if not current_user.is_following(user_to_unfollow):
                return {"message": "You are not following this user"}, 400
            
            current_user.unfollow(user_to_unfollow)
            db.session.commit()
            return {"message": f"You have unfollowed {user_to_unfollow.name}"}, 200
        except Exception as e:
            return {"message": "Internal server error"}, 500