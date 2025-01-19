from telegram import Update
from telegram.ext import ContextTypes
from database import dep_balance, get_user, withdraw_funds
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

async def admin_withdraw_funds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        target_id = int(context.args[0])
        amount = float(context.args[1])

        # Проверяем, достаточно ли средств для вывода
        user = get_user(target_id)
        if not user or user[2] < amount:
            await update.message.reply_text("❌ У пользователя недостаточно средств для вывода.")
            return

        # Выполняем вывод средств
        success = withdraw_funds(target_id, amount)

        if success:
            # Уведомление администратора
            await update.message.reply_text(f"✅ Вывод {amount}₽ пользователю с ID {target_id} выполнен успешно.")

            # Уведомление пользователя
            try:
                await context.bot.send_message(
                    chat_id=target_id,
                    text=(
                        f"💸 Ваш запрос на вывод средств обработан. На ваш счет, в течении 24 часов поступят средства в размере {amount:.2f}₽."
                    )
                )
            except Exception as e:
                await update.message.reply_text(f"⚠️ Не удалось отправить уведомление пользователю с ID {target_id}: {e}")
        else:
            await update.message.reply_text("❌ Ошибка при выполнении вывода средств. Попробуйте снова.")

    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /withdraw_funds <user_id> <amount>")


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

        # Уведомление пользователя
        try:
            await context.bot.send_message(
                chat_id=target_id,
                text=(
                    f"🔔 Ваш статус верификации изменён администратором.\n"
                    f"Текущий статус: {status_text}."
                )
            )
        except Exception as e:
            await update.message.reply_text(f"⚠️ Не удалось отправить уведомление пользователю с ID {target_id}: {e}")

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

# Команда для массовой рассылки сообщений
async def admin_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        message_text = " ".join(context.args)  # Сообщение для рассылки

        if not message_text:
            await update.message.reply_text("❌ Сообщение для рассылки не может быть пустым.")
            return

        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]

        conn.close()

        sent_count = 0
        for target_id in user_ids:
            try:
                await context.bot.send_message(
                    chat_id=target_id,
                    text=message_text
                )
                sent_count += 1
            except Exception as e:
                print(f"⚠️ Не удалось отправить сообщение пользователю с ID {target_id}: {e}")

        await update.message.reply_text(f"✅ Сообщение успешно отправлено {sent_count} пользователям.")

    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при выполнении рассылки: {e}")

# Команда для получения информации о пользователе
async def admin_get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    try:
        target_id = int(context.args[0])
        user = get_user(target_id)

        if not user:
            await update.message.reply_text("❌ Пользователь не найден.")
            return

        verification_status = "✅" if user[8] else "❌"

        caption = (
            f"💻 Информация о пользователе:\n\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"📑 Верификация: {verification_status}\n"
            f"🗄 ID: `{user[0]}`\n"
            f"💵 Баланс: {user[2]}₽\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"ℹ️ Статистика пользователя:\n"
            f"┏ Всего сделок проведено: {user[3]}\n"
            f"┣ Неудачных: {user[5]}\n"
            f"┣ Удачных: {user[4]}\n"
            f"┗ Выводов совершено {user[6]} на сумму {user[7]}₽\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
        )

        await update.message.reply_text(caption, parse_mode="Markdown")

    except (IndexError, ValueError):
        await update.message.reply_text("❌ Использование: /user_info <user_id>")

# Команда для отображения всех команд администратора
async def admin_commands_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not await is_admin(user_id):
        await update.message.reply_text("❌ У вас нет прав для выполнения этой команды.")
        return

    commands = (
        "📜 *Список команд администратора:*\n\n"
        "1. /add_balance <user_id> <amount> - Пополнить баланс пользователя.\n"
        "   Пример: `/add_balance 12345 500`\n\n"
        "2. /withdraw_funds <user_id> <amount> - Вывести средства пользователю.\n"
        "   Пример: `/withdraw_funds 12345 500`\n\n"
        "3. /verify_user <user_id> <0|1> - Изменить статус верификации пользователя.\n"
        "   Пример: `/verify_user 12345 1`\n\n"
        "4. /set_balance <user_id> <new_balance> - Установить новый баланс пользователю.\n"
        "   Пример: `/set_balance 12345 1000`\n\n"
        "5. /broadcast <message> - Отправить сообщение всем пользователям.\n"
        "   Пример: `/broadcast Добрый день, мы рады вас видеть!`\n\n"
        "6. /user_info <user_id> - Получить информацию о пользователе.\n"
        "   Пример: `/user_info 12345`\n\n"
    )

    await update.message.reply_text(commands, parse_mode="Markdown")