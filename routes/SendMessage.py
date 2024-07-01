from flask import request, jsonify, make_response
from flask_restful import Resource
from datetime import datetime

from lib import db, User, Message

class SendMessage(Resource):
    def send_message():
        data = request.get_json()
        
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')
        
        if not sender_id or not receiver_id or not content:
            return jsonify({'error': 'Missing sender_id, receiver_id, or content'}), 400
        
        sender = User.query.get(sender_id)
        receiver = User.query.get(receiver_id)
        
        if not sender or not receiver:
            return jsonify({'error': 'Sender or receiver does not exist'}), 404
        
        try:
            new_message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content,
            )   
        
            db.session.add(new_message)
            db.session.commit()
            
            return jsonify({'message': 'Message sent successfully'}), 201
        except Exception as e:
            db.session.rollback()
            response = make_response(
                jsonify({"An error occured:", str(e)}), 500
            )
            return response
