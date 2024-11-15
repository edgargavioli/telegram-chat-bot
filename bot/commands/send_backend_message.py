from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests
import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

sio.connect('ws://127.0.0.1:5000/', transports=['polling'])

from config import API_URL

async def updates_to_backend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    message = update.message.text

    client_exists = requests.get(f"{API_URL}/clients/bot{chat_id}")

    if client_exists.status_code != 200:
        return
    
    data = {
        "chat_id": chat_id,
        "message": message
    }

    sio.emit('new_message', data)