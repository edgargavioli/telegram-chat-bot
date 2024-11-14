from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests

from config import API_URL

async def client_register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat.id
    name = update.message.chat.first_name

    client_exists = requests.get(f"{API_URL}/clients/bot{chat_id}")

    if client_exists.status_code == 200:
        return
    
    data = {
        "chat_id": chat_id,
        "name": name
    }

    requests.post(f"{API_URL}/clients/start", json=data)