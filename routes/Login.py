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
        
        # Check if password is correct
        if not user.check_password(password):
            abort(401, description="Wrong password")

        # Set user ID in session
        session["user_id"] = user.id
        
        # Create JWT access token
        access_token = create_access_token(identity=user, expires_delta=timedelta(days=1))
        
        # Return response with the token
        response = make_response( 
            jsonify({
                "name": user.name,
                "role_id": user.role_id,
                "access_token": access_token
            }), 200)
        
        # Set cookie if needed
        response.set_cookie('access_token', access_token, httponly=True)

        return response