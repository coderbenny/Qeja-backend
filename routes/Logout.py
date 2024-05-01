from flask import jsonify, session, make_response
from flask_restful import Resource

class Logout(Resource):
    
    def delete(self):
        
        # if "user_id" not in session:
        #     return {"error": "User is not logged in"}, 403
        
        # session.pop("user_id")
        # response.set_cookie("session", "", expires=0)
        return {}, 200
