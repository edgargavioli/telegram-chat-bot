from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, InlineQueryHandler, CallbackContext, MessageHandler, filters
import requests
from commands.client import client_register
from commands.catalog import catalog_command
from commands.catalog import handle_callback_query
from commands.cart import cart_command, button
from config import TOKEN, BOT_USERNAME, API_URL

async def responder_palavra_chave(update: Update, context: CallbackContext):
    mensagem = update.message.text.lower()
    palavras_chave = ["catalog"]
    
    for palavra in palavras_chave:
        if palavra in mensagem:
            if palavra == "catalog":
                await catalog_command(update, context)
    
        else:
            await update.message.reply_text("Desculpe, não entendi sua mensagem.")

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await client_register(update, context)
    await update.message.reply_text("Online shop :)")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Bot is running")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("catalog", catalog_command))
    app.add_handler(CommandHandler("cart", cart_command))

    app.add_handler(CallbackQueryHandler(handle_callback_query))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_palavra_chave))

    app.add_error_handler(error)

    print("Bot is polling")
    app.run_polling()