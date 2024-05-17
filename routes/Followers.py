from flask import jsonify, request, make_response
from flask_restful import Resource
from lib import db, User

class Followers(Resource):
    
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        followers = user.followers.all()
        response = make_response(
            jsonify([{'id': follower.id, 'name': follower.name} for follower in followers]),
            200
        )
        
        return response