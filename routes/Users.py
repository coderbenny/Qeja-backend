from flask import jsonify, make_response, request
from flask_restful import Resource
from lib import db, User

class Users(Resource):
    
    def get(self):
        users = User.query.all()
        
        if not users:
            return {"error": "No users found"}

        response_data = []
        for user in users:
            user_dict = {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role_id": user.role_id,
                "profile": user.profile.to_dict() if user.profile else None
            }
            response_data.append(user_dict)

        response = make_response(jsonify(response_data), 200)
        
        return response
        
    
    def post(self):
        data = request.get_json()
        
        if not data:
            return {"error":"Invalid data"}, 400
        
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role_id = data.get("role_id")
        
        if not all([name, email, password, role_id]):
            return {"error":"Invalid user data"}, 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            return {"error":"user exists"}, 409
        
        try:
            new_user = User(name=name, email=email, password=password, role_id=role_id)
            db.session.add(new_user)
            db.session.commit()
            
            
            response = make_response(
                jsonify(new_user.to_dict()), 
                201
            )
            return response
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
