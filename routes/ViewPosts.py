from flask import jsonify, make_response, request
from flask_restful import Resource
from lib import db, Post

class ViewPosts(Resource):
    
    def get(self):
        posts = Post.query.all()
        
        if not posts:
            return {"error":"No posts found"}

        response = make_response(
            jsonify([p.to_dict() for p in posts]),
            200
        )
        
        return response
        
    
    def post(self):
        data = request.get_json()
        
        if not data:
            return {"error":"Invalid data"}, 400
        
        user_id = data.get("user_id")
        body = data.get("body")
        image = data.get("image")
        
        if not all([user_id, body]):
            return {"error":"Invalid user data"}, 400
        
        try:
            new_post = Post(user_id=user_id, body=body, image=image)
            db.session.add(new_post)
            db.session.commit()
            
            
            response = make_response(
                jsonify(new_post.to_dict()), 
                201
            )
            return response
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500
