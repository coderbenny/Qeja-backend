from flask import jsonify, make_response
from flask_restful import Resource
from lib import User
from flask_jwt_extended import jwt_required


class RoomMates(Resource):
    # @jwt_required()
    def get(self):
        mates = User.query.filter_by(role_id=3).all()
        
        if not mates:
            return {"error":"Room mates not found"}, 404
    
        response_data = []
        for mate in mates:
            user_dict = {
                "id": mate.id,
                "name": mate.name,
                "email": mate.email,
                "profile": mate.profile.to_dict() if mate.profile else None
            }
            response_data.append(user_dict)

        response = make_response(jsonify(response_data), 200)
        
        return response