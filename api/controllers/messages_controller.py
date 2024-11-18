import requests
import os
from functools import wraps
from flask import Blueprint, jsonify, request
from app.routes.login import current_user
from api.models.db import db
from api.models.messages import Messages

messages_bp = Blueprint('messages', __name__, url_prefix='/api')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@messages_bp.route('/messages', methods=['GET'])
@login_required
def get_messages():
    messages = Messages.query.all()
    return jsonify([{
        'id': message.id,
        'chat_id': message.chat_id,
        'message': message.message,
        'type': message.type
    }for message in messages])

@messages_bp.route('/messages/send', methods=['POST'])
@login_required
def send_telegram_message():
    data = request.get_json()

    chat_id = data.get('chat_id')
    message = data.get('message')
    type = data.get('type')
    token = os.getenv('TELEGRAM_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    print(chat_id, message)

    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    if type == 'transmitir':
        response = requests.post(url, data=payload)
        return


    try:
        db.session.add(Messages(chat_id=chat_id, message=message, type='sent'))
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    response = requests.post(url, data=payload)
    return response.json()

def receive_telegram_message(chat_id, message):
    try:
        db.session.add(Messages(chat_id=chat_id, message=message, type='received'))
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'message': 'Message received'}), 200