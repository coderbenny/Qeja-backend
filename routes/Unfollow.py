from flask import request, session
from flask_restful import Resource

from lib import db, User

class Unfollow(Resource):

    def post(self, user_id):
        current_user_id = request.json.get('current_user_id')
        user_to_unfollow = User.query.get(user_id)
        current_user = User.query.get(current_user_id)
        
        if not user_to_unfollow:
            return {'error': 'User to unfollow not found'}, 404
        
        if not current_user:
            return {'error': 'Current user not found'}, 404

        if current_user.is_following(user_to_unfollow):
            current_user.unfollow(user_to_unfollow)
            db.session.commit()
            return {'message': 'You have unfollowed this user'}, 200
        else:
            return {'message': 'You already unfollowed this user'}, 200