from flask import Blueprint, jsonify, make_response
from flask_restful import Api, Resource
from lib import db, User
from flask_jwt_extended import jwt_required

mates_bp = Blueprint("mates_bp", __name__)
api = Api(mates_bp)

class MatesResource(Resource):

    # Fetching mates from db
    # @jwt_required()
    def get(self, id=None):
        if not id:
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
        
        # Fetching a single user from the db
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"error":"User does not exist!"}, 404
        
        response = make_response(
            jsonify(user.to_dict()),
            200
        )

        return response

    
    # Deleting a user
    # @jwt_required()
    def delete(self, id):
        mate = User.query.filter(User.role_id == 3, User.id == id).first()
        
        if not mate:
            return {"error":"Room mate does not exist"}, 404

        try:
            db.session.delete(mate)
            db.session.commit()
            return {"success":"User deleted successfully"}, 204
        except Exception as e:
            db.session.rollback()
            response = make_response(
                jsonify({"error:", str(e)}), 
                500
            )
            return response
        
api.add_resource(MatesResource, "/roommates", "/roommates/<int:id>")