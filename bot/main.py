from typing import Final
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext, MessageHandler, filters
import requests
from commands.client import client_register
from commands.catalog import catalog_command
from commands.catalog import handle_callback_query
from commands.cart import cart_command, button
from commands.send_backend_message import updates_to_backend
from config import TOKEN, BOT_USERNAME, API_URL
from commands.human import human_conversation, modo_humano_ativo
from config import TOKEN, BOT_USERNAME, API_URL, waiting_address, waiting_number, waiting_city

customer_messages = {}
clients = {}

async def responder_palavra_chave(update: Update, context: CallbackContext):
    keyboard = []

    keyboard.append([
        InlineKeyboardButton(text='Cancelar ❌', callback_data='cancelar'),
        InlineKeyboardButton(text='Confirmar ✅', callback_data='confirmar')
    ])

    reply_markup = InlineKeyboardMarkup(keyboard)

    mensagem = update.message.text.lower()
    userId = update.message.from_user.id
    palavras_chave = ["catalog"]

    if userId in modo_humano_ativo and modo_humano_ativo[userId]:
        if mensagem == "sair":
            modo_humano_ativo[userId] = False
            return
        customer_messages[userId] = mensagem
        await updates_to_backend(update, context)
        return

    if userId in waiting_city and waiting_city[userId]:
        waiting_city[userId] = False
        if userId not in clients:
            clients[userId] = {}
        clients[userId]['city'] = mensagem
        print(f"Client city for {userId}: {clients[userId]['city']}")
        
        waiting_address[userId] = True
        await update.message.reply_text("Agora, digite seu endereço de entrega.")
        return

    if userId in waiting_address and waiting_address[userId]:
        waiting_address[userId] = False
        if userId not in clients:
            clients[userId] = {}
        clients[userId]['address'] = mensagem
        print(f"Client address for {userId}: {clients[userId]['address']}")
        
        waiting_number[userId] = True
        await update.message.reply_text("Agora, digite seu número de telefone.")
        return

    if userId in waiting_number and waiting_number[userId]:
        waiting_number[userId] = False
        if userId not in clients:
            clients[userId] = {}
        clients[userId]['phone_number'] = mensagem
        print(f"Client number for {userId}: {clients[userId]['phone_number']}")
        
        print(f"Updating client {userId} with data: {clients[userId]}")
        response = requests.put(f"{API_URL}/clients/bot{userId}", json=clients[userId])
        print(f"Response: {response.json()}")
        await update.message.reply_text("Número recebido! Obrigado por completar o checkout. Aperte o botão para confirmar o pedido", reply_markup=reply_markup)
        return

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
    app.add_handler(CommandHandler("human", human_conversation))

    app.add_handler(CallbackQueryHandler(handle_callback_query))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_palavra_chave))

    app.add_error_handler(error)

    print("Bot is polling")
    app.run_polling()
