from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
from io import BytesIO

TOKEN: Final = "7715292562:AAHBcryB9C1m26GWjTSRe4GLkiFPdE14AuM"
BOT_USERNAME = "@piveta_delivery_bot"

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Online shop :)")

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get("http://web:5000/api/products")

    if response.status_code == 200:
        await update.message.reply_text("Catalog:")
        for product in response.json():
            # image_response = requests.get("http://172.19.0.3:5000/static/img/produtos/Tux.svg.png")
            # if image_response.status_code == 200:
            #     photo = BytesIO(image_response.content)
            #     await update.message.reply_photo(photo=photo)
            await update.message.reply_text(f"{product['name']} - {product['price']}")
    else:
        await update.message.reply_text("Failed to load catalog.")
    print(response.json())

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Bot is running")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("catalog", catalog_command))

    app.add_error_handler(error)

    print("Bot is polling")
    app.run_polling()
