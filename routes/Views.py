from flask import jsonify, request
from flask_restful import Resource
from lib import db, View

class Views(Resource):
    
    def post(self, post_id):
        user_id = request.json.get('user_id')
        view = View(post_id=post_id, user_id=user_id)
        db.session.add(view)
        db.session.commit()
        return jsonify(view.to_dict()), 201