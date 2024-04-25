from flask import jsonify, make_response
from flask_restful import Resource
from lib import Role

class Roles(Resource):
    
    def get(self):
        roles = Role.query.all()
        
        if not roles:
            return {"error":"Roles not found"}, 404
    
        response = make_response(
            jsonify([r.to_dict() for r in roles]),
            200
        )
        return response