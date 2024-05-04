from flask import make_response, jsonify
from flask_restful import Resource
from lib import db, Property
from flask_jwt_extended import jwt_required


class PropertyByID(Resource):
    
    # @jwt_required()
    def get(self, id):
        property = Property.query.filter_by(id=id).first()
            
        if not property:
            return {"error":"Property does not exist"}, 404

        response = make_response(
            jsonify(property.to_dict(view_owner=True)),
            200
        )
        
        return response
    
    
    def delete(self, id):
        property = Property.query.filter_by(id=id).first()
            
        if not property:
            return {"error":"Property does not exist"}, 404
    
        try:
            db.session.delete(property)
            db.session.commit()
            return {"success": "deleted succesfully"}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
