from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, InlineQueryHandler
import requests
from commands.catalog import catalog_command
from commands.catalog import handle_callback_query
from config import TOKEN, BOT_USERNAME, API_URL

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Online shop :)")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Bot is running")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("catalog", catalog_command))

    app.add_handler(CallbackQueryHandler(handle_callback_query))

    app.add_error_handler(error)

    print("Bot is polling")
    app.run_polling()