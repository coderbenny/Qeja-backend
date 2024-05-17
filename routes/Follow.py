from flask import jsonify, request, session
from flask_restful import Resource

from lib import db, User

class Follow(Resource):
    
    def post(self, user_id):
        current_user_id = request.json.get('current_user_id')
        user_to_follow = User.query.get(user_id)
        current_user = User.query.get(current_user_id)
        
        if user_to_follow and current_user:
            current_user.follow(user_to_follow)
            db.session.commit()
            return {'message': 'You are now following this user'}, 200
        return {'error': 'User not found'}, 404
