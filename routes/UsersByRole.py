from flask import jsonify, make_response
from flask_restful import Resource
from lib import db, User

class UsersByRole(Resource):
    
    def get(self, roleId):
        users = User.query.filter_by(role_id=roleId).all()
            
        if not users:
            return {"error":"User role does not exist"}

        response = make_response(
            jsonify([u.to_dict(view_property=True) for u in users]),
            200
        )
        
        return response
    
    
    