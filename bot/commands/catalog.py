from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from io import BytesIO
import requests
import json

from config import API_URL, IMG_PREFIX, cart, waiting_address, waiting_city, waiting_number
from datetime import datetime

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
        waiting_city[user_id] = True 
        await query.message.reply_text("Digite sua cidade")
    elif query.data == 'clear_cart':
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
    elif query.data == "checkout_address":
        await query.message.reply_text("Digite seu endereço de entrega:")
        endereco = update.message.text
    elif query.data == "confirmar":
        print("Pedido confirmado")
        total_amount = 0.0

        for item in cart[user_id].values():
            quantity = item['quantity']
            price = item['price']
            total_amount += quantity * price

        order = {
            "created_date": datetime.now().date().strftime("%Y-%m-%d"),
            "created_time": datetime.now().strftime("%H:%M:%S"),
            "status": "Em espera",
            "amount": total_amount
        }

        print(order)

        response = requests.post(f"{API_URL}/orders/bot{user_id}", json=order)

        if response.status_code == 200:
            print("Pedido criado com sucesso:", response.json())
            order_response = response.json()
            
            # Acessando o id corretamente dentro de 'Order'
            order_id = order_response['Order']['id']
            print(order_id)
            
            if order_id:
                for item_id, item in cart[user_id].items():
                    print(item)
                    order_item = {
                        "order_id": order_id,  # Usando o id correto
                        "product_id": item_id,
                        "quantity": item['quantity'],
                        "product_price": item['price'],
                        "product_name": item['product_name']
                    }
                    print(order_item)
                    
                    # Enviando a solicitação para criar o item de pedido
                    response = requests.post(f"{API_URL}/orders_items", json=order_item)
                    
                    if response.status_code == 201:
                        print("Item de pedido criado com sucesso:", response.json())
                    else:
                        print(f"Erro ao criar item de pedido: {response.status_code}, {response.text}")
            else:
                print("Sem id na response")
        else:
            print(f"Erro ao criar pedido: {response.status_code}, {response.text}")



    elif query.data == "cancelar":
        await query.message.reply_text("Seu pedido foi cancelado.")

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
