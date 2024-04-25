from flask import jsonify, make_response
from flask_restful import Resource
from lib import db, Property

class Properties(Resource):
    
    def get(self):
        properties = Property.query.all()
        
        if not properties:
            return {"error":"No properties found"}

        response = make_response(
            jsonify([p.to_dict() for p in properties]),
            200
        )
        
        return response
        
    
    def post(self):
        return "Route for adding a property"
    
