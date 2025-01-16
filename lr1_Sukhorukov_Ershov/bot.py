import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import Database

# Токен вашего бота
TELEGRAM_BOT_TOKEN = '7513564407:AAEFyyu8bW279JlIqpUFHkP2UI0TseUbpEA'

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    db = Database()
    if not db.get_user(chat_id):
        db.save_user(chat_id, username, first_name, last_name)

    # Кнопка Deposit
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Deposit", callback_data="show_deposit_buttons")]]
    )

    await update.message.reply_text(
        f"Здравствуйте, {first_name}! Ваш текущий баланс: {db.get_balance(chat_id)} рублей.\n"
        f"Нажмите на кнопку ниже, чтобы пополнить баланс.",
        reply_markup=keyboard
    )
    db.close()

# Обработчик для кнопки Deposit
async def show_deposit_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Кнопки для выбора суммы пополнения
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("100 рублей", callback_data="deposit_100")],
        [InlineKeyboardButton("500 рублей", callback_data="deposit_500")],
        [InlineKeyboardButton("1000 рублей", callback_data="deposit_1000")],
        [InlineKeyboardButton("5000 рублей", callback_data="deposit_5000")],
    ])

    await query.edit_message_text(
        "Выберите сумму для пополнения:",
        reply_markup=keyboard
    )

# Обработчик для пополнения баланса
async def handle_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Определяем сумму из callback_data
    deposit_mapping = {
        "deposit_100": 100,
        "deposit_500": 500,
        "deposit_1000": 1000,
        "deposit_5000": 5000,
    }
    amount = deposit_mapping.get(query.data, 0)

    if amount > 0:
        chat_id = query.from_user.id
        db = Database()
        user = db.get_user(chat_id)
        if user:
            # Обновляем баланс пользователя
            db.update_balance(chat_id, amount)
            new_balance = db.get_balance(chat_id)
            await query.edit_message_text(f"Ваш баланс пополнен на {amount} рублей!\nТекущий баланс: {new_balance} рублей.")
        else:
            await query.edit_message_text("Вы не зарегистрированы. Используйте команду /start.")
        db.close()
    else:
        await query.edit_message_text("Ошибка! Некорректная сумма пополнения.")

# Запуск бота
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_deposit_buttons, pattern="^show_deposit_buttons$"))
    application.add_handler(CallbackQueryHandler(handle_deposit, pattern="^deposit_"))

    # Запуск бота
    loop.run_until_complete(application.run_polling())

