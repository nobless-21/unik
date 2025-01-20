import asyncio
import random
import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import Database

# Токен вашего бота
TELEGRAM_BOT_TOKEN = '7513564407:AAEFyyu8bW279JlIqpUFHkP2UI0TseUbpEA'


# Функция отправки уведомления пользователю о новой роли (асинхронная версия)
def send_admin_notification(chat_id):
    message = "Поздравляем! Вы были назначены администратором."
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }

    # Используем requests для отправления POST-запроса
    response = requests.post(url, data=payload)

    if response.status_code != 200:
        print(f"Ошибка при отправке сообщения: {response.text}")
    else:
        print(f"Сообщение отправлено пользователю {chat_id}: {message}")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    username = update.message.chat.username
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name

    db = Database()
    if not db.get_user(chat_id):
        db.save_user(chat_id, username, first_name, last_name)

    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("Сделать ставку", callback_data="choose_bet")]])

    await update.message.reply_text(
        f"Здравствуйте, {first_name}! Ваш текущий баланс: {db.get_balance(chat_id)} рублей.\n"
        "Нажмите на кнопку ниже, чтобы сделать ставку.",
        reply_markup=keyboard
    )
    db.close()

async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    db = Database()

    # Проверяем, является ли пользователь администратором
    if not db.is_admin(chat_id):
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")
        db.close()
        return

    # Получаем статистику
    user_count = len(db.get_all_users())  # Получаем количество пользователей
    bet_count = len(db.get_all_bets())    # Получаем количество ставок

    # Формируем сообщение для админа
    stat_message = f"Количество пользователей: {user_count}\nКоличество ставок: {bet_count}"

    # Отправляем статистику администратору
    await update.message.reply_text(stat_message)

    db.close()


# Выбор коэффициента для ставки
async def choose_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Коэффициент 1.5", callback_data="coef_1.5")],
        [InlineKeyboardButton("Коэффициент 2.0", callback_data="coef_2.0")],
        [InlineKeyboardButton("Коэффициент 3.0", callback_data="coef_3.0")],
        [InlineKeyboardButton("Коэффициент 5.0", callback_data="coef_5.0")],
    ])

    await query.edit_message_text(
        "Выберите коэффициент для ставки:",
        reply_markup=keyboard
    )


# Обработка выбора коэффициента
async def handle_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    coefficient = float(query.data.split("_")[1])

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("100 рублей", callback_data=f"bet_{coefficient}_100")],
        [InlineKeyboardButton("500 рублей", callback_data=f"bet_{coefficient}_500")],
        [InlineKeyboardButton("1000 рублей", callback_data=f"bet_{coefficient}_1000")],
        [InlineKeyboardButton("5000 рублей", callback_data=f"bet_{coefficient}_5000")],
    ])

    await query.edit_message_text(
        f"Вы выбрали коэффициент {coefficient}. Теперь выберите сумму для ставки:",
        reply_markup=keyboard
    )


# Результат ставки
async def finalize_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    _, coefficient, amount = query.data.split("_")
    coefficient = float(coefficient)
    amount = int(amount)

    chat_id = query.from_user.id
    db = Database()

    balance = db.get_balance(chat_id)
    if balance < amount:
        await query.edit_message_text("Недостаточно средств для ставки. Пополните баланс.")
        db.close()
        return

    win_probability = 1 / coefficient
    is_win = random.random() < win_probability

    if is_win:
        win_amount = int(amount * coefficient)
        db.update_balance(chat_id, win_amount)
        db.save_bet(chat_id, amount, coefficient, "WIN")
        await query.edit_message_text(
            f"Поздравляем! Вы выиграли {win_amount} рублей!\nВаш текущий баланс: {db.get_balance(chat_id)} рублей."
        )
    else:
        db.update_balance(chat_id, -amount)
        db.save_bet(chat_id, amount, coefficient, "LOSE")
        await query.edit_message_text(
            f"Вы проиграли {amount} рублей.\nВаш текущий баланс: {db.get_balance(chat_id)} рублей."
        )

    db.close()


# Пополнение баланса
async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    db = Database()

    try:
        if len(context.args) != 1:
            await update.message.reply_text("Укажите сумму для пополнения. Пример: /deposit 1000")
            return

        amount = int(context.args[0])

        if amount <= 0:
            await update.message.reply_text("Сумма должна быть больше 0.")
            return

        user = db.get_user(chat_id)
        if user:
            db.update_balance(chat_id, amount)
            new_balance = db.get_balance(chat_id)
            await update.message.reply_text(
                f"Ваш баланс успешно пополнен на {amount} рублей.\nТекущий баланс: {new_balance} рублей."
            )
        else:
            await update.message.reply_text("Вы не зарегистрированы. Используйте команду /start.")
    except ValueError:
        await update.message.reply_text("Сумма должна быть числом. Пример: /deposit 1000")
    finally:
        db.close()


# Пример функции для назначения пользователя администратором
async def set_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    db = Database()

    # Присваиваем пользователю роль администратора
    db.set_admin(chat_id, is_admin=True)

    # Отправляем уведомление пользователю о новой роли
    await send_admin_notification(chat_id)

    await update.message.reply_text("Вы были назначены администратором.")

    db.close()


# Запуск бота
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("deposit", deposit))
    application.add_handler(CallbackQueryHandler(choose_bet, pattern="^choose_bet$"))
    application.add_handler(CallbackQueryHandler(handle_bet, pattern="^coef_"))
    application.add_handler(CallbackQueryHandler(finalize_bet, pattern="^bet_"))
    application.add_handler(CommandHandler("set_admin", set_admin))  # Новый обработчик для назначения администратора
    application.add_handler(CommandHandler("stat", stat))

    loop.run_until_complete(application.run_polling())
