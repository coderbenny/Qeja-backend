from flask import jsonify, make_response, request
from flask_restful import Resource
from lib import db, User, Profile

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

    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"error": "User does not exist"}, 404
        
        data = request.get_json()
        profile = user.profile or Profile(user_id=user.id)
        
        # Update profile fields if provided in the request
        profile.bio = data.get("bio", profile.bio)
        profile.location = data.get("location", profile.location)
        profile.profile_pic = data.get("profile_pic", profile.profile_pic)

        try:
            db.session.add(profile)  # Add profile to session if it was newly created
            db.session.commit()
            response = make_response(
                jsonify(user.profile.to_dict()), 
                200
            )
            return response
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500