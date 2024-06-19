from flask import jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

from lib import User

class Whoami(Resource):
    @jwt_required()
    def get(self):
        profile_dict = current_user.profile.to_dict() if current_user.profile else None
        response = make_response(
            jsonify(
                id=current_user.id,
                name=current_user.name,
                email=current_user.email,
                role_id=current_user.role_id,
                profile=profile_dict
            ),
            200
        )
        return response
