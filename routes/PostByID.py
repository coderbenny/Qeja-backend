from flask import make_response, jsonify
from flask_restful import Resource
from lib import db, Post
from flask_jwt_extended import jwt_required


class PostByID(Resource):
    
    # @jwt_required()
    def get(self, id):
        post = Post.query.filter_by(id=id).first()
            
        if not post:
            return {"error":"Post does not exist"}, 404

        response = make_response(
            jsonify(post.to_dict()),
            200
        )
        
        return response
    
    
    def delete(self, id):
        post = Post.query.filter_by(id=id).first()
            
        if not post:
            return {"error":"Post does not exist"}, 404
    
        try:
            db.session.delete(post)
            db.session.commit()
            return {"success": "deleted succesfully"}, 204
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
