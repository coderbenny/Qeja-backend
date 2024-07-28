from flask import jsonify, make_response, request
from flask_restful import Resource
from flask_mail import Message
from random import randint
from lib import db, User
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
            # Generate activation code
            activation_code = f'{randint(100000, 999999):06d}'

            new_user = User(name=name, email=email, password=password, role_id=role_id, activation_code=activation_code)
            db.session.add(new_user)
            db.session.commit()

            # Send activation email
            # msg = Message(subject='Your Qeja Account Activation', recipients=[email])
            # msg.html = f"""
            # <html>
            #     <body>
            #         <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto;">
            #             <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; border: 1px solid #e9ecef;">
            #                 <h2 style="color: #343a40;">Welcome to Qeja!</h2>
            #                 <p>Hello {name},</p>
            #                 <p>Thank you for registering with Qeja. To complete your registration, please use the following activation code:</p>
            #                 <p style="font-size: 20px; font-weight: bold;">{activation_code}</p>
            #                 <p>If you did not request this registration, please ignore this email.</p>
            #                 <p>Best regards,</p>
            #                 <p>The Qeja Team</p>
            #             </div>
            #             <div style="text-align: center; margin-top: 20px; color: #6c757d; font-size: 12px;">
            #                 <p>&copy; 2024 Qeja, Inc. All rights reserved.</p>
            #             </div>
            #         </div>
            #     </body>
            # </html>
            # """
            # mail.send(msg)

            response = make_response(
                jsonify(new_user.to_dict()),
                201
            )
            return response
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

# Adding the Users resource to the API
# api.add_resource(Users, '/users', resource_class_args=(mail,))
