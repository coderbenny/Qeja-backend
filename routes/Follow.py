from flask import jsonify, request, session
from flask_restful import Resource

from lib import db, User

class Follow(Resource):
    
    def post(self, user_id):
        current_user_id = request.json.get('current_user_id')
        user_to_follow = User.query.get(user_id)
        current_user = User.query.get(current_user_id)
        
        if not user_to_follow:
            return {'error': 'User to follow not found'}, 404
        
        if not current_user:
            return {'error': 'Current user not found'}, 404

        if current_user.is_following(user_to_follow):
            return {'message': 'You are already following this user'}, 200

        try:
            current_user.follow(user_to_follow)
            db.session.commit()
            return {'message': 'You are now following this user'}, 200
        except Exception as e:
            db.session.rollback()
            return {"error":str(e)}, 500