from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from io import BytesIO
import requests

from config import API_URL, IMG_PREFIX, cart

async def cart_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    
    user_cart = cart.get(user_id, {})
    
    if not user_cart:
        await update.message.reply_text("Seu carrinho está vazio.")
    else:
        total = 0
        text = "Seu carrinho:\n"
        for item_id, cart_item in user_cart.items():
            product_name = cart_item['product_name']
            price = cart_item['price']
            quantity = cart_item['quantity']
            item_total = price * quantity
            text += f"{product_name} - {quantity} pcs. - {item_total} $\n"
            total += item_total
        
        text += f"Total: {total} R$"
        
        keyboard = [
            [InlineKeyboardButton("Checkout", callback_data='checkout')],
            [InlineKeyboardButton("Limpar Carrinho", callback_data='clear_cart')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'checkout':
        # await query.message.reply_text(text="Indo para o checkout...")
        await query.message.reply_text(text="Digite seu endereço de entrega:", callback_data='checkout_address')

        # Lógica de checkout aqui
    elif query.data == 'clear_cart':
        # Limpar o carrinho do usuário
        if user_id in cart:
            cart[user_id].clear()
        await query.edit_message_text(text="Seu carrinho foi limpo.")

