from flask import jsonify, request
from flask_restful import Resource

from lib import db, Impression

class Impressions(Resource):
    def post(self, post_id):
        user_id = request.json.get('user_id')
        impression = Impression(post_id=post_id, user_id=user_id)
        db.session.add(impression)
        db.session.commit()
        return jsonify(impression.to_dict()), 201