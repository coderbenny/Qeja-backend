from flask_restful import Resource

class UserByID(Resource):
    
    def get(self, id):
        return "Users By ID will be here"
    
    
    def delete(self, id):
        return "Route for deleting User By ID"
    
