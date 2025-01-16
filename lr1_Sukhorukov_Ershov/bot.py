import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import Database

# Токен вашего бота
TELEGRAM_BOT_TOKEN = '7513564407:AAEFyyu8bW279JlIqpUFHkP2UI0TseUbpEA'

# Функция для команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    db = Database()
    if not db.get_user(chat_id):
        db.save_user(chat_id, username, first_name, last_name)

    await update.message.reply_text(f"Здраствуйте, {first_name}! Какой депозит вы хотите внести?")
    db.close()

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    loop.run_until_complete(application.run_polling())
