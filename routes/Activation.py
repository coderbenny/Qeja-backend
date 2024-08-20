from flask import request, jsonify
from flask_restful import Resource
from lib import db, User

class Activation(Resource):

    def post(self):
        data = request.get_json()
        email = data.get('email')
        activation_code = data.get('activation_code')

        if not data or not all([email, activation_code]):
            return {'message': 'Email and activation code are required'}, 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return {'message': 'User not found'}, 404

        if user.is_active:
            return {'message': 'User is already activated. Proceed to login'}, 200

        if user.activation_code != activation_code:
            return {'message': 'Invalid activation code'}, 400
        
        try:
            user.is_active = True
            user.activation_code = None  
            db.session.commit()
            return {'message': 'Account activated successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {"error":str(e)}, 500
