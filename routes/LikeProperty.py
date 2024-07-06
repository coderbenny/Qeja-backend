from flask import jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from lib import db, Property, User

class LikeProperty(Resource):
    @jwt_required()
    def post(self, property_id):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        property = Property.query.get(property_id)

        if not user or not property:
            return jsonify({'message': 'User or Property not found'}), 404

        user.like_property(property)
        db.session.commit()  # Commit the transaction once

        return jsonify({'message': f'User {current_user_id} liked Property {property_id}'}), 200
