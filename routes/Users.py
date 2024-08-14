from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_mail import Message
from random import randint
from lib import db, User, Profile
from extensions import mail

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
                "is_active": user.is_active,
                "profile": user.profile.to_dict() if user.profile else None
            }
            response_data.append(user_dict)

        response = make_response(jsonify(response_data), 200)
        return response

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
            # # Generate activation code
            # activation_code = f'{randint(100000, 999999):06d}'

            new_user = User(name=name, email=email, password=password, role_id=role_id, activation_code=activation_code)
            
            activation_code = f'{randint(100000, 999999):06d}'

            new_user.activation_code = activation_code
            self.send_activation_email(new_user.name, new_user.email, activation_code)

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
        
    # Route for deleting a user
    def delete(self, id):
        pass

    # Function for sending email
    def send_activation_email(self, name, recipient, activation_code):
        msg = Message(
            subject='Your Account Activation Code',
            sender="Qeja <qeja.ke@gmail.com>",
            recipients=[recipient]
        )
        msg.html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f4f4f4;">
                    <div style="max-width: 600px; margin: 40px auto; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);">
                        <div style="text-align: center;">
                            <img src="https://your-logo-url.com/logo.png" alt="Qeja Logo" style="width: 120px; margin-bottom: 20px;">
                        </div>
                        <div style="background-color: #f8f9fa; padding: 30px; border-radius: 5px; border: 1px solid #e9ecef;">
                            <h2 style="color: #343a40; text-align: center;">Welcome to Qeja!</h2>
                            <p style="color: #343a40;">Hello {name},</p>
                            <p style="color: #343a40;">Thank you for registering with Qeja. To complete your registration, please use the following activation code:</p>
                            <p style="font-size: 24px; font-weight: bold; text-align: center; color: #007bff;">{activation_code}</p>
                            <p style="color: #343a40;">If you did not request this registration, please ignore this email.</p>
                            <p style="color: #343a40;">Best regards,</p>
                            <p style="color: #343a40;">The Qeja Team</p>
                        </div>
                        <div style="text-align: center; margin-top: 30px; color: #6c757d; font-size: 12px;">
                            <p>&copy; 2024 Qeja, Inc. All rights reserved.</p>
                            <p><a href="https://qeja.com/privacy-policy" style="color: #007bff; text-decoration: none;">Privacy Policy</a> | <a href="https://qeja.com/terms" style="color: #007bff; text-decoration: none;">Terms of Service</a></p>
                        </div>
                    </div>
                </body>
            </html>
        """

        try:
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send activation email: {str(e)}")
    

    

# Adding the Users resource to the API
# api.add_resource(Users, '/users', resource_class_args=(mail,))
