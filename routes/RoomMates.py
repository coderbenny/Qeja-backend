from flask import jsonify, make_response
from flask_restful import Resource
from lib import User

class RoomMates(Resource):
    
    def get(self):
        mates = User.query.filter_by(role_id=3).all()
        
        if not mates:
            return {"error":"Room mates not found"}, 404
    
        response = make_response(
            jsonify([r.to_dict() for r in mates]),
            200
        )
        return response