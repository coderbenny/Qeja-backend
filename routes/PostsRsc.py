from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from lib import Post, db, User
from flask_jwt_extended import jwt_required, get_jwt_identity

posts_bp = Blueprint("posts_bp", __name__)
api = Api(posts_bp)


class PostsResource(Resource):
    def get(self, id=None):
        if id:
            post = Post.query.get(id)
            if not post:
                return {"message": "Post not found"}, 404
            return jsonify(post.to_dict()), 200
        
        posts = Post.query.all()
        if not posts:
            return {"message":"Posts not found"}, 404
        return jsonify([post.to_dict() for post in posts])

    @jwt_required
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        
        if not data:
            return {"error":"Invalid data"}, 400
        
        if not user_id:
            return {"error":"User ID does not exist"}, 404
        
        content=data.get('content'),
        # pic1=data.get('pic1')
        # pic2=data.get('pic2')
        # pic3=data.get('pic3')

        if not data or not all([user_id, content]):
            return {"error": "Invalid data"}, 400
    
        user = User.query.get(user_id)
        
        if not user:
            return {"message": "User not found"}, 404

        try:
            post = Post(
                user_id=user.id,
                content=content,
            )
            db.session.add(post)
            db.session.commit()

            return {"success":"Post created succesfully"}, 200
        except Exception as e:
            db.session.rollback()
            res =  make_response({"An error occured":str(e)}, 500)
            return res

    def put(self, id):
        post = Post.query.get(id)
        if not post:
            return {"message": "Post not found"}, 404

        data = request.get_json()
        post.content = data.get('content', post.content)
        post.pic1 = data.get('pic1', post.pic1)
        post.pic2 = data.get('pic2', post.pic2)
        post.pic3 = data.get('pic3', post.pic3)
        db.session.commit()

        return jsonify(post.to_dict())

    def delete(self, id):
        post = Post.query.get(id)
        if not post:
            return {"message": "Post not found"}, 404

        db.session.delete(post)
        db.session.commit()
        return {"message": "Post deleted successfully"}, 200


api.add_resource(PostsResource, "/posts", "/posts/<int:id>")