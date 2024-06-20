from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from lib import User

class Whoami(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return {"error": "User does not exist"}, 404
        
        user_data = user.to_dict(view_property=True)
        
        response = make_response(jsonify(user_data), 200)
        return response
        
