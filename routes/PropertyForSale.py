from flask import make_response, jsonify
from flask_restful import Resource
from lib import db, Property
from flask_jwt_extended import jwt_required


class PropertyForSale(Resource):
    
    # @jwt_required()
    def get(self):
        properties = Property.query.filter_by(for_rent=False).all()
            
        if not properties:
            return {"error":"Properties does not exist"}, 404

        response = make_response(
            jsonify([prop.to_dict(view_owner=True) for prop in properties]),
            200
        )
        
        return response
    
