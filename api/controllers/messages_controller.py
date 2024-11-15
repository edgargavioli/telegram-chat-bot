import requests
import os
from functools import wraps
from flask import Blueprint, jsonify, request
from app.routes.login import current_user
from flask_socketio import SocketIO

messages_bp = Blueprint('messages', __name__, url_prefix='/api')
socketio = SocketIO(cors_allowed_origins="*")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@messages_bp.route('/messages/send', methods=['POST'])
@login_required
def send_telegram_message():
    data = request.get_json()

    chat_id = data.get('chat_id')
    message = data.get('message')
    token = os.getenv('TELEGRAM_TOKEN')
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    print(chat_id, message)
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    return response.json()

@messages_bp.route('/messages/receive', methods=['POST'])
def receive_telegram_message():
    update = request.json

    if not update:
        return {"error": "Invalid update"}, 400
    
    # Processar a atualização recebida
    print(f"Received update: {update}")

    socketio.emit('new_message', update)
    
    # Aqui você pode armazenar no banco, processar ou enviar para o frontend
    return {"status": "Update processed"}, 200