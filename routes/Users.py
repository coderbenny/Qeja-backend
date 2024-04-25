from flask_restful import Resource

class Users(Resource):
    
    def get(self):
        return "All Users will be here"
    
    
    def post(self):
        return "Route for adding users"
    
