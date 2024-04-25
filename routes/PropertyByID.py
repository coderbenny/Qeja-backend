from flask_restful import Resource

class PropertyByID(Resource):
    
    def get(self, id):
        return "Property by ID will be here"
    
    
    def delete(self, id):
        return "Route for deleting Property By ID"
    
