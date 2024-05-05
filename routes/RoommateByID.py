from flask import jsonify, make_response
from flask_restful import Resource
from lib import User
from flask_jwt_extended import jwt_required


class RoommateByID(Resource):
    # @jwt_required()
    def get(self,id):
        mate = User.query.filter(User.role_id == 3, User.id == id).first()
        
        if not mate:
            return {"error":"Room mate does not exist"}, 404
    
        response = make_response(
            jsonify(mate.to_dict()),
            200
        )
        return response