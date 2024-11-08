from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, MenuButton
from telegram.ext import Application, CommandHandler, ContextTypes
from io import BytesIO
import requests

from config import API_URL, IMG_PREFIX

PRODUCT_QUANTITY_CALLBACK = "catalog=product-quantity"
MINUS_PRODUCT_CALLBACK = "catalog=minus-product_"
PLUS_PRODUCT_CALLBACK = "catalog=plus-product_"
OPEN_CATALOG_CALLBACK = "catalog=open-catalog"
OPEN_CART_CALLBACK = "catalog=open-cart"

def build_keyboard(product, cart_item=None):
    keyboard = []

    if cart_item:
        keyboard.append([
            InlineKeyboardButton(text='➖', callback_data=f'{MINUS_PRODUCT_CALLBACK}{product["id"]}'),
            InlineKeyboardButton(text=f'{cart_item.quantity} pcs.', callback_data=PRODUCT_QUANTITY_CALLBACK),
            InlineKeyboardButton(text='➕', callback_data=f'{PLUS_PRODUCT_CALLBACK}{product["id"]}')
        ])
        keyboard.append([
            InlineKeyboardButton(text="Catalog", callback_data=OPEN_CATALOG_CALLBACK),
            InlineKeyboardButton(text="Cart", callback_data=OPEN_CART_CALLBACK)
        ])
    else:
        keyboard.append([
            InlineKeyboardButton(text=f'💵 Price: {product["price"]} $ 🛍 Add to cart', callback_data=f'{PLUS_PRODUCT_CALLBACK}{product["id"]}')
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
    await query.answer()

    if query.data.startswith("category="):
        category_id = query.data.split("=")[1]
        
        response = requests.get(f"{API_URL}/categories/{category_id}/product")
        
        if response.status_code == 200:
            products = response.json()
            
            if products and isinstance(products, list):
                for product in products:
                    if all(k in product for k in ['name', 'price', 'id', 'photo_url']):
                        keyboard = build_keyboard(product)
                        image_response = requests.get(f"{IMG_PREFIX}{product['photo_url']}")
                        if image_response.status_code == 200:
                            photo = BytesIO(image_response.content)
                            await query.message.reply_photo(photo=photo)
                        else:
                            await query.message.reply_text(f"Product: {product['name']}\nPrice: {product['price']} $ (No Image Available)", reply_markup=keyboard)
                        await query.message.reply_text(
                            text=f"{product['name']}\nPrice: {product['price']} $",
                            reply_markup=keyboard
                        )
                    else:
                        await query.message.reply_text("Some product data is incomplete.")
            else:
                await query.message.reply_text("No products found for this category.")
        else:
            await query.message.reply_text("Failed to load products for the selected category.")
    
    # Process other callbacks for cart operations (like adding/removing products)
    elif query.data.startswith("catalog="):
        await handle_cart_operations(query)

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(f"{API_URL}/categories")

    if response.status_code == 200:
        categories = response.json()
        
        if categories and isinstance(categories, list):
            await update.message.reply_text("Catalog:", reply_markup=build_category_keyboard(categories=categories))
        else:
            await update.message.reply_text("No categories available.")
    else:
        await update.message.reply_text("Failed to load catalog.")
    
    print(response.json()) if response.status_code == 200 else print("Error loading categories")

async def handle_cart_operations(query):
    data = query.data
    if data.startswith(MINUS_PRODUCT_CALLBACK):
        product_id = data.split('_')[1]
        # Lógica para diminuir a quantidade do produto no carrinho
        await query.answer(f"Product {product_id} decreased.")
    elif data.startswith(PLUS_PRODUCT_CALLBACK):
        product_id = data.split('_')[1]
        # Lógica para aumentar a quantidade do produto no carrinho
        await query.answer(f"Product {product_id} increased.")
