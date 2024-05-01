from flask import jsonify, request, session, abort, make_response
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from datetime import timedelta
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
        
        session["user_id"] = user.id
        access_token = create_access_token(identity=user.email)
        
        # expiry = timedelta(days=1)
        
        response = make_response(
            jsonify({"name":user.name,"role_id":user.role_id,"access_token":access_token}),
            200
        )
        response.set_cookie('access_token', access_token, httponly=True)
        return response
        
        