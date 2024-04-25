from flask import make_response, jsonify
from flask_restful import Resource
from lib import db, Property

class PropertyByID(Resource):
    
    def get(self, id):
        property = Property.query.filter_by(id=id).first()
            
        if not property:
            return {"error":"Property does not exist"}

        response = make_response(
            jsonify(property.to_dict(view_owner=True)),
            200
        )
        
        return response
    
    
    def delete(self, id):
        return "Route for deleting Property By ID"
    
