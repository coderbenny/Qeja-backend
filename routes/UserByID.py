from flask import jsonify, make_response
from flask_restful import Resource
from lib import db, User

class UserByID(Resource):
    
    def get(self, id):
        user = User.query.filter_by(id=id).first()
            
        if not user:
            return {"error":"User does not exist"}

        response = make_response(
            jsonify(user.to_dict(view_property=True)),
            200
        )
        
        return response
    
    
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
            
        if not user:
            return {"error":"User does not exist"}

        try:
            db.session.delete(user)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
