from flask import request, jsonify, make_response
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
        data = request.get_json()
        
        if not data:
            return {"error":"Invalid data"}, 400
        
        pic1 = data.get("pic1") 
        pic2 = data.get("pic2") 
        pic3 = data.get("pic3") 
        description = data.get("description") 
        location = data.get("location")
        rent = data.get("rent")
        amenities = data.get("amenities") 
        wifi = data.get("wifi")
        gated = data.get("gated")
        hot_shower = data.get("hot_shower")
        kitchen = data.get("kitchen")
        balcony = data.get("balcony")
        parking = data.get("parking")
        user_id = data.get("user_id")
    
        if not all([pic1, pic2, pic3, description, location, rent, wifi, gated, hot_shower, kitchen, balcony, parking, user_id]):
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
