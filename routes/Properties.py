from flask_restful import Resource

class Properties(Resource):
    
    def get(self):
        return "Properties will be here"
    
    
    def post(self):
        return "Route for adding a property"
    
