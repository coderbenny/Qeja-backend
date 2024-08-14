from flask import Blueprint, jsonify, request, make_response
from flask_restful import Api, Resource
from lib import User, Profile, db
from random import randint
from flask_mail import Message
from extensions import mail

users_bp = Blueprint("users_bp", __name__)
api = Api(users_bp)

class UsersResource(Resource):
    
    # Retrieving user(s) from the database
    def get(self, id):
        if not id:
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
                    "is_active": user.is_active,
                    "profile": user.profile.to_dict() if user.profile else None,
                    "followers":[u.id for u in user.followers], 
                    "following": [u.id for u in user.followed]
                }
                response_data.append(user_dict)

            response = make_response(jsonify(response_data), 200)
            return response
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"error":"User not found!"}, 404
        
        response = make_response(
            jsonify({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role_id": user.role_id,
                    "is_active": user.is_active,
                    "profile": user.profile.to_dict() if user.profile else None,
                    "followers":[u.id for u in user.followers], 
                    "following": [u.id for u in user.followed]
                }),
            200
        )

        return response
    
    # Adding new user & sending activation to email
    def post(self):
        data = request.get_json()

        if not data:
            return {"error": "Invalid data"}, 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role_id = data.get("role_id")

        if not all([name, email, password, role_id]):
            return {"error": "Invalid user data"}, 400

        user = User.query.filter_by(email=email).first()
        if user:
            return {"error": "User exists"}, 409

        try:
            # Generate activation code
            activation_code = f'{randint(100000, 999999):06d}'

            new_user = User(name=name, email=email, password=password, role_id=role_id, activation_code=activation_code)
            db.session.add(new_user)
            db.session.commit()

            # Send activation email
            msg = Message(subject='Your Qeja Account Activation Code', sender="Qeja <Qeja.ke@gmail.com>", recipients=[email])
            msg.html = f"""
            <html>
                <body>
                    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; background-color: #f4f4f4; padding: 20px;">
                        <div style="background-color: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
                            <h2 style="color: #343a40; text-align: center; margin-bottom: 20px;">Welcome to Qeja!</h2>
                            <p style="font-size: 16px; color: #343a40;">Hello {name},</p>
                            <p style="font-size: 16px; color: #343a40;">Thank you for registering with Qeja. To complete your registration, please use the following activation code:</p>
                            <p style="font-size: 24px; font-weight: bold; text-align: center; margin: 20px 0; color: #007bff;">{activation_code}</p>
                            <p style="font-size: 16px; color: #343a40;">If you did not request this registration, please ignore this email.</p>
                            <p style="font-size: 16px; color: #343a40;">Best regards,</p>
                            <p style="font-size: 16px; color: #343a40;">The Qeja Team</p>
                        </div>
                        <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
                            <p>&copy; 2024 Qeja, Inc. All rights reserved.</p>
                        </div>
                    </div>
                </body>
            </html>
            """

            mail.send(msg)

            response = make_response(
                jsonify(new_user.to_dict()),
                201
            )
            return response
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
    
    # Deleting user
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

    # Changing user details
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
        
    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"error":"User does not exist"}, 404
        
        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

api.add_resource(UsersResource, "/users", "/users/<int:id>")
