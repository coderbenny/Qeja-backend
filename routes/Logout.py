from flask import jsonify, session, make_response
from flask_restful import Resource

class Logout(Resource):
    
    def delete(self):
        
        if "user" not in session:
            return jsonify({"error": "User is not logged in"}), 403
        
        session.pop("user")        
        response = make_response(jsonify({"success": "Logged out successfully"}), 200)
        
        # response.set_cookie("session", "", expires=0)
        return response
