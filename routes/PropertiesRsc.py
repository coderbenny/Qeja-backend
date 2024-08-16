from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from lib import db, Property
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity

properties_bp = Blueprint("properties_bp", __name__)
api = Api(properties_bp)

class PropertiesResource(Resource):

    # Retrieving properties from db
    # @jwt_required()    
    def get(self, id=None):
        if id:
            property = Property.query.filter_by(id=id).first()
            
            if not property:
                return {"error":"Property does not exist"}, 404

            response = make_response(
                jsonify(property.to_dict(view_owner=True)),
                200
            )
            
            return response
    
        properties = Property.query.all()
        
        if not properties:
            return {"error":"No properties found"}

        response = make_response(
            jsonify([p.to_dict() for p in properties]),
            200
        )
        
        return response
        
    # Adding property
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not user_id:
            return {"error":"Invalid data"}, 400
        
        pic1 = data.get("pic1") 
        pic2 = data.get("pic2") 
        pic3 = data.get("pic3") 
        description = data.get("description") 
        location = data.get("location")
        rent = data.get("rent")
        wifi = data.get("wifi")
        gated = data.get("gated")
        hot_shower = data.get("hot_shower")
        kitchen = data.get("kitchen")
        balcony = data.get("balcony")
        parking = data.get("parking")
        available = data.get("available")
        rooms = data.get("rooms")
        user_id = user_id
    
        if not all([ description, location, rent, wifi, gated, available, rooms, user_id]):
            return {"error":"Invalid data"}, 400
        
        try:
            new_property = Property(
                pic1=pic1, 
                pic2=pic2, 
                pic3=pic3,
                description=description,
                location=location,
                rent=rent,
                wifi=wifi,
                parking=parking,
                gated=gated,
                hot_shower=hot_shower,
                kitchen=kitchen,
                balcony=balcony,
                available=available,
                user_id=user_id
                )
            
            db.session.add(new_property)
            db.session.commit()
            
            response = make_response(
                jsonify(new_property.to_dict(view_owner=True)),
                201
            )
            
            return response
        except Exception as e:
            db.session.rollback()
            return {"error":"An error occurred"}, 500
        
    
    # Deleting property
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


    # Change property details 
    def patch(self, id):
        property = Property.query.filter_by(id=id).first()

        if not property:
            return {"error": "Property does not exist"}, 404

        data = request.get_json()
        if not data:
            return {"error": "Invalid data"}, 400

        # Only update the fields that are provided in the request
        if 'description' in data:
            property.description = data['description']
        if 'rent' in data:
            property.rent = data['rent']
        if 'wifi' in data:
            property.wifi = data['wifi']
        if 'gated' in data:
            property.gated = data['gated']
        if 'hot_shower' in data:
            property.hot_shower = data['hot_shower']
        if 'kitchen' in data:
            property.kitchen = data['kitchen']
        if 'balcony' in data:
            property.balcony = data['balcony']
        if 'parking' in data:
            property.parking = data['parking']
        if 'available' in data:
            property.available = data['available']
        if 'rooms' in data:
            property.rooms = data['rooms']

        try:
            db.session.commit()
            response = make_response(
                jsonify(property.to_dict(view_owner=True)),
                200
            )
            return response
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
        

api.add_resource(PropertiesResource, "/properties","/properties/<int:id>")
