from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import requests

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

    requests.post(f"{API_URL}/messages/receive", json=data)

    # async def updates_to_backend(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     data = {
    #         "update_id": update.update_id,
    #         "message": update.message.to_dict() if update.message else None,
    #         "callback_query": update.callback_query.to_dict() if update.callback_query else None,
    #         "inline_query": update.inline_query.to_dict() if update.inline_query else None,
    #     }
    #     response = requests.post(f"{API_URL}/updates", json=data)
    #     if response.status_code != 200:
    #         print(f"Failed to send update to backend: {response.status_code}")