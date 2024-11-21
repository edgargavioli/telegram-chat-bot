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
    name = update.message.from_user.first_name
    chat_id = update.message.chat.id
    message = update.message.text
    
    data = {
        "chat_id": chat_id,
        "message": message,
        "name": name
    }

    sio.emit('new_message', data)