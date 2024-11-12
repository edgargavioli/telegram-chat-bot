from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from io import BytesIO
import requests

from config import API_URL, IMG_PREFIX, cart

PRODUCT_QUANTITY_CALLBACK = "catalog=product-quantity"
MINUS_PRODUCT_CALLBACK = "catalog=minus-product_"
PLUS_PRODUCT_CALLBACK = "catalog=plus-product_"
OPEN_CATALOG_CALLBACK = "catalog=open-catalog"
OPEN_CART_CALLBACK = "catalog=open-cart"

# Função para construir o teclado do produto
def build_keyboard(product, cart_item=None):
    keyboard = []

    if cart_item:
        keyboard.append([
            InlineKeyboardButton(text='➖', callback_data=f'{MINUS_PRODUCT_CALLBACK}{product["id"]}'),
            InlineKeyboardButton(text=f'{cart_item["quantity"]} pcs.', callback_data=PRODUCT_QUANTITY_CALLBACK),
            InlineKeyboardButton(text='➕', callback_data=f'{PLUS_PRODUCT_CALLBACK}{product["id"]}')
        ])
        keyboard.append([
            InlineKeyboardButton(text="Catálogo", callback_data=OPEN_CATALOG_CALLBACK),
            InlineKeyboardButton(text="Carrinho", callback_data=OPEN_CART_CALLBACK)
        ])
    else:
        keyboard.append([
            InlineKeyboardButton(text=f'💵 Preço: {product["price"]} $ 🛍 Adicionar ao carrinho', callback_data=f'{PLUS_PRODUCT_CALLBACK}{product["id"]}')
        ])

    return InlineKeyboardMarkup(keyboard)

def build_category_keyboard(categories):
    keyboard = []

    for category in categories:
        keyboard.append([
            InlineKeyboardButton(text=category['name'], callback_data=f"category={category['id']}")
        ])

    return InlineKeyboardMarkup(keyboard)

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    data = query.data

    if query.data == 'checkout':
        await query.message.reply_text("Indo para o checkout...")
        # Lógica de checkout aqui
    elif query.data == 'clear_cart':
        # Limpar o carrinho do usuário
        if user_id in cart:
            cart[user_id].clear()
        await query.message.reply_text("Seu carrinho foi limpo.")

    if query.data.startswith("category="):
        category_id = query.data.split("=")[1]
        
        response = requests.get(f"{API_URL}/categories/{category_id}/product")
        
        if response.status_code == 200:
            products = response.json()
            
            if products and isinstance(products, list):
                for product in products:
                    if all(k in product for k in ['name', 'price', 'id', 'photo_url']):
                        keyboard = build_keyboard(product, cart.get(query.from_user.id, {}).get(str(product['id'])))
                        image_response = requests.get(f"{IMG_PREFIX}{product['photo_url']}")
                        if image_response.status_code == 200:
                            photo = BytesIO(image_response.content)
                            await query.message.reply_photo(photo=photo)
                        await query.message.reply_text(
                            text=f"{product['name']}\nPreço: {product['price']} $",
                            reply_markup=keyboard
                        )
            else:
                await query.message.reply_text("Nenhum produto encontrado para esta categoria.")
        else:
            await query.message.reply_text("Falha ao carregar produtos para a categoria selecionada.")
    
    elif query.data.startswith("catalog="):
        await handle_cart_operations(query)

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f"{API_URL}/categories")

    if response.status_code == 200:
        categories = response.json()
        
        if categories and isinstance(categories, list):
            await update.message.reply_text("Catalog:", reply_markup=build_category_keyboard(categories=categories))
        else:
            await update.message.reply_text("Sem categorias cadastradas.")
    else:
        await update.message.reply_text("Algo deu errado ao buscar o catálogo.")
    
    print(response.json()) if response.status_code == 200 else print("Error loading categories")

async def handle_cart_operations(query):
    data = query.data
    chat_id = query.message.chat_id

    if chat_id not in cart:
        cart[chat_id] = {}

    if data.startswith(MINUS_PRODUCT_CALLBACK):
        product_id = data.split('_')[1]
        if product_id in cart[chat_id]:
            if cart[chat_id][product_id]['quantity'] > 1:
                cart[chat_id][product_id]['quantity'] -= 1
            else:
                del cart[chat_id][product_id]
        await query.answer(f"Product {product_id} decreased.")
    elif data.startswith(PLUS_PRODUCT_CALLBACK):
        product_id = data.split('_')[1]
        product_name = query.message.text.split('\n')[0]
        product_price = float(query.message.text.split('\n')[1].split(' ')[1])
        
        if product_id in cart[chat_id]:
            cart[chat_id][product_id]['quantity'] += 1
        else:
            cart[chat_id][product_id] = {
                'quantity': 1,
                'product_name': product_name,
                'price': product_price
            }
        
        await query.message.reply_text(f"O produto {product_name} foi adicionado ao carrinho. Quantidade: {cart[chat_id][product_id]['quantity']}")

        await query.answer(f"Product {product_name} increased.")
        print(cart)
