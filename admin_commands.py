from telegram import Update
from telegram.ext import ContextTypes
from database import dep_balance
import sqlite3
import config

# Проверка, является ли пользователь администратором
async def is_admin(user_id):
    admins = config.amd
    return user_id in admins

# Команда пополнения баланса
async def admin_add_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        target_id = int(context.args[0])
        amount = float(context.args[1])
        dep_balance(target_id, amount)

        # Уведомление администратора
        await update.message.reply_text(f"✅ Баланс пользователя с ID {target_id} пополнен на {amount}₽.")

        # Уведомление пользователя
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"💳 Ваш баланс был успешно пополнен на {amount:.2f}₽ администрацией.\n"
                    f"Проверьте ваш текущий баланс."
                )
            )
        except Exception as e:
            await update.message.reply_text(f"⚠️ Не удалось отправить уведомление пользователю с ID {target_id}: {e}")

    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /add_balance <user_id> <amount>")

# Команда изменения статуса верификации
async def admin_verify_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        target_id = int(context.args[0])
        status = bool(int(context.args[1]))  # 0 или 1
        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users SET verif = ? WHERE id = ?
        ''', (status, target_id))

        conn.commit()
        conn.close()

        status_text = "верифицирован" if status else "не верифицирован"
        await update.message.reply_text(f"✅ Статус верификации пользователя с ID {target_id} изменен на: {status_text}.")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /verify_user <user_id> <status (0 или 1)>")

# Команда изменения баланса напрямую
async def admin_set_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        target_id = int(context.args[0])
        new_balance = float(context.args[1])

        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET balance = ? WHERE id = ?
        ''', (new_balance, target_id))

        conn.commit()
        conn.close()

        await update.message.reply_text(f"✅ Баланс пользователя с ID {target_id} установлен на {new_balance}₽.")
    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /set_balance <user_id> <new_balance>")
