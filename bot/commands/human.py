from telegram import Update
from telegram.ext import CallbackContext

modo_humano_ativo = {}

async def human_conversation(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    modo_humano_ativo[user_id] = True
    await update.message.reply_text("Envie sua dúvida ou problema que logo um funcionário irá te ajudar.")
    await update.message.reply_text("Digite 'sair' para sair do modo humano.")