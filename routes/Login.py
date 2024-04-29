from flask import jsonify, request, session, abort, make_response
from flask_restful import Resource

from lib import User

class Login(Resource):
    
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        if not data or not all([email, password]):
            abort(400, description="Invalid user credentials")
        
        user = User.query.filter_by(email=email).first()
        if not user:
            abort(404, description="User does not exist")
        
        if user.password != password:
            abort(401, description="Wrong password")
        
        session["user"] = {"name": user.name, "email": user.email, "role_id": user.role_id}
        
        response = make_response(
            jsonify({
                "name": user.name,
                "email": user.email,
                "role_id": user.role_id
            }), 200)
        return response
