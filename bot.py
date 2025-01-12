# bot.py

# Импортируем необходимые модули и классы из библиотеки `python-telegram-bot`
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Импортируем функции для работы с базой данных и обработки торгов
from database import init_db, add_user, get_user, update_balance, process_trade, withdraw_funds

# Импортируем модуль для генерации случайных чисел
import random

# Используется для получения текущего курса криптовалют
import requests

# Импортируем токен бота из конфигурационного файла
from config import BOT_TOKEN

# Инициализация базы данных при запуске бота
init_db()

# Функция для получения текущего курса криптовалюты
def get_crypto_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data[symbol]['usd']
    except Exception as e:
        print(f"Ошибка получения курса {symbol}: {e}")
        return None


# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем информацию о пользователе, который вызвал команду /start
    user = update.effective_user
    
    # Добавляем пользователя в базу данных, если его там еще нет
    add_user(user.id, user.username)

    # Создаем меню кнопок (Reply Keyboard) для основного интерфейса
    reply_keyboard = [
        ["💼 Личный Кабинет", "🔷 О сервисе"],
        ["🧑🏻‍💻 Тех.Поддержка", "📊 Опционы"]
    ]
    reply_markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)

    # Отправляем приветственное сообщение с меню кнопок
    await update.message.reply_text(
        f"Привет, {user.username}! Добро пожаловать в бота. Выберите действие:",
        reply_markup=reply_markup
    )

# Обработчик текстовых сообщений
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем текст сообщения и ID пользователя
    text = update.message.text
    user_id = update.message.from_user.id

    # Обрабатываем различные текстовые команды
    if text in ("💼 Личный Кабинет", "⬅️ Назад в личный кабинет"):
        # Получаем информацию о пользователе из базы данных
        user = get_user(user_id)
        if user:
            # Путь к изображению для личного кабинета
            image = "./assets/project-1.jpg"
            
            # Формируем текст сообщения с информацией о пользователе
            caption = (
                f"💻 Личный кабинет:\n\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"📑 Верификация: ❌\n"
                f"🗄 ID: {user[0]}\n"
                f"💵 Баланс: {user[2]}₽\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"ℹ️ Статистика пользователя:\n"
                f"┏ Всего сделок проведено: {user[3]}\n"
                f"┣ Неудачных: {user[5]}\n"
                f"┣ Удачных: {user[4]}\n"
                f"┗ Выводов совершено {user[6]} на сумму {user[7]}₽\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
                f"_Откройте двери в мир криптовалют вместе с CoinWizard - Вашим верным спутником в онлайн трейдинге на финансовых рынках._"
            )
            
            # Создаем инлайн-кнопки для личного кабинета
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("💳 Пополнить", callback_data="replenish"), InlineKeyboardButton("🏦 Вывести", callback_data="withdraw")],
                [InlineKeyboardButton("🗃 Верификация", callback_data="verify"), InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
                [InlineKeyboardButton("Мои активы", callback_data="my_assets")]
            ])

            # Отправляем изображение с текстом и инлайн-кнопками
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        else:
            # Если пользователь не найден, отправляем сообщение об ошибке
            await update.message.reply_text("Ошибка: пользователь не найден.")

    elif text == "🔷 О сервисе":
        # Формируем текст с информацией о сервисе
        service_text = (
            "*CoinWizard* - централизованная биржа для торговли криптовалютой и фьючерсными активами.\n\n"
            "🔹 *Ведущие инновации*\n"
            "┗ Мы не стоим на месте и находимся в постоянном стремлении к совершенству. Внедрение передовых решений и установление новых тенденций делает нас лидерами отрасли.\n\n"
            "🔹 *Лояльность клиентов*\n"
            "┗ Доступная каждому возможность стать профессиональным трейдером. Установление долгосрочных отношений за счет отзывчивости и регулярного оказания первоклассных услуг.\n\n"
            "🔹 *Общий успех*\n"
            "┗ Наша задача — предоставлять клиентам по всему миру простую и доступную торговлю, которая позволяет зарабатывать на финансовых рынках в любое время и в любом месте.\n\n"
            "Благодаря простому пользовательскому интерфейсу *CoinWizard* прекрасно подходит для новичков. На платформе легко ориентироваться, что привлекает как продвинутых, так и начинающих трейдеров и инвесторов."
        )

        # Создаем инлайн-кнопки
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📖 Условия", callback_data="service_terms"), InlineKeyboardButton("📜 Сертификат", callback_data="service_certificate")],
            [InlineKeyboardButton("Гарантия сервиса", callback_data="service_guarantee"), InlineKeyboardButton("📈 Состояние сети", callback_data="service_network")],
            [InlineKeyboardButton("⚙️ Реферальная система", callback_data="service_referral")]
        ])

        # Отправляем сообщение с текстом и кнопками
        await update.message.reply_text(service_text, reply_markup=keyboard, parse_mode="Markdown")
        
    elif text == "🧑🏻‍💻 Тех.Поддержка":
        # Формируем текст для обращения в техподдержку
        support_text = (
            "📘 Вы можете открыть заявку в службу поддержки CoinWizard. Специалист ответит Вам в ближайшие сроки.\n"
            "Для более быстрого решения проблемы описывайте возникшую проблему максимально четко. "
            "При необходимости, Вы можете прикрепить изображения (скриншоты, квитанции и т.д.)\n\n"
            "Правила обращения в тех. поддержку:\n\n"
            "1. Пожалуйста, представьтесь при первом обращении.\n"
            "2. Описывайте проблему своими словами, но как можно подробнее.\n"
            "3. Если возможно, прикрепите скриншот, на котором видно, в чём заключается Ваша проблема.\n"
            "4. Пришлите Ваш ID личного кабинета, дабы ускорить решение проблемы.\n"
            "5. Относитесь к агенту поддержки с уважением. Не грубите ему и не дерзите, если заинтересованы в скорейшем разрешении Вашего вопроса."
        )

        # Создаем инлайн-кнопку для перехода в чат с техподдержкой
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📩 Написать", url="https://t.me/durov")] # Поменяйте ссылку на свой аккаунт
        ])

        # Отправляем сообщение с текстом и кнопкой
        await update.message.reply_text(support_text, reply_markup=keyboard)

    elif text == "📊 Опционы":
        # Формируем текст с информацией о опционах
        options_text = (
            "_Опционы - это финансовые инструменты, которые дают инвестору право, но не обязательство, купить или продать определенное количество акций или других активов по определенной цене в определенный момент в будущем.\n\n_"
            "*💠 Выберите монету для инвестирования денежных средств:*"
        )

        # Создаем инлайн-кнопки с выбором криптовалют
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("BTC", callback_data="option_btc"), InlineKeyboardButton("ETH", callback_data="option_eth")],
            [InlineKeyboardButton("BNB", callback_data="option_bnb"), InlineKeyboardButton("XRP", callback_data="option_xrp")],
            [InlineKeyboardButton("ADA", callback_data="option_ada"), InlineKeyboardButton("SOL", callback_data="option_sol")],
            [InlineKeyboardButton("DOGE", callback_data="option_doge"), InlineKeyboardButton("DOT", callback_data="option_dot")],
        ])

        # Отправляем сообщение с текстом и кнопками
        await update.message.reply_text(options_text, reply_markup=keyboard, parse_mode="Markdown")
        
    elif context.user_data.get("awaiting_withdrawal"):
        try:
            amount = float(text)  # Преобразуем введенный текст в число
            if amount < 1000:
                await update.message.reply_text("❌ Минимальная сумма вывода: 1000₽.")
            else:
                # Пытаемся выполнить вывод средств
                success = withdraw_funds(user_id, amount)
                if success:
                    # Сообщение об успешном выводе
                    await update.message.reply_text(f"✅ Вывод {amount}₽ успешно выполнен!")
                else:
                    # Сообщение о недостатке средств
                    await update.message.reply_text("❌ Недостаточно средств на балансе.")
                    
        except ValueError:
            await update.message.reply_text("❌ Введите корректную сумму.")
        
        # Сбрасываем состояние "ожидание ввода суммы вывода"
        context.user_data["awaiting_withdrawal"] = False
        return  # Важно: завершаем выполнение, чтобы не перейти к другим условиям


    else:
        # Если текст сообщения не распознан, отправляем сообщение с просьбой выбрать опцию
        await update.message.reply_text("Я не понял ваш запрос. Попробуйте выбрать одну из доступных опций.")
        

# Обработчик инлайн-кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем данные из callback-запроса
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()  # Подтверждаем получение callback-запроса

    # Обрабатываем различные callback_data
    if query.data == "replenish":
        # Формируем текст и кнопки для пополнения баланса
        text = "💳 *Выберите вариант пополнения баланса:*"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Пополнить через банковскую карту", callback_data="deposit_card")],
            [InlineKeyboardButton("Пополнить криптовалютой", callback_data="deposit_crypto")],
            [InlineKeyboardButton("Ввести промокод", callback_data="deposit_promo")]
        ])
        # Обновляем сообщение с новым текстом и кнопками
        await query.edit_message_caption(caption=text, reply_markup=keyboard, parse_mode="Markdown")

    elif query.data == "deposit_card":
        # Генерируем случайную сумму для пополнения через карту
        amount = random.randint(5000, 50000)
        update_balance(user_id, amount)
        user = get_user(user_id)
        if user:    
            text = (
                f"💳 *Пополнение успешно!*\n\n"
                f"На ваш баланс добавлено {amount}₽.\n"
                f"Текущий баланс: {user[2]}₽."
            )
        else:
            text = "❌ *Ошибка:* Пользователь не найден."

        # Обновляем сообщение с результатом пополнения
        await query.edit_message_caption(caption=text, parse_mode="Markdown")

    elif query.data == "deposit_crypto":
        # Генерируем случайную сумму для пополнения криптовалютой
        amount = random.randint(100000, 300000)
        update_balance(user_id, amount)
        user = get_user(user_id)

        if user:
            text = (
                f"💵 *Пополнение успешно!*\n\n"
                f"На ваш баланс добавлено {amount}₽ криптовалютой.\n"
                f"Текущий баланс: {user[2]}₽."
            )
        else:
            text = "❌ *Ошибка:* Пользователь не найден."

        # Обновляем сообщение с результатом пополнения
        await query.edit_message_caption(caption=text, parse_mode="Markdown")

    elif query.data == "deposit_promo":
        # Запрашиваем ввод промокода
        text = "🎟️ *Введите промокод:*\nПожалуйста, введите ваш промокод для активации баланса."
        await query.edit_message_caption(caption=text, parse_mode="Markdown")
        
    elif query.data == "my_assets":
        # Формируем текст с информацией о текущих активах
        text = (
            "💼 *Активы:*\n\n"
            "Активы - это финансовые инструменты, которые трейдеры покупают или продают на рынке для получения прибыли. "
            "Это могут быть различные виды финансовых инструментов, включая акции, валюты, сырьевые товары, облигации, опционы и другие.\n\n"
            "🗄 *Активы:*\n"
            "┏ BTC: 0.0\n"
            "┣ ETH: 0.0\n"
            "┣ USDT: 0.0\n"
            "┣ SHIB: 0.0\n"
            "┗ ATOM: 0.0"
        )

        # Создаем инлайн-кнопки для управления активами
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Покупка", callback_data="buy_assets"), InlineKeyboardButton("Продажа", callback_data="sell_assets")],
            [InlineKeyboardButton("Трейд", callback_data="trade_assets")]
        ])

        # Обновляем сообщение с новым текстом и кнопками
        await query.edit_message_caption(caption=text, reply_markup=keyboard, parse_mode="Markdown")
        
    elif query.data == "buy_assets":
        # Запрашиваем выбор актива для покупки
        text = "🛒 *Выберите актив для покупки:*\nBTC, ETH, USDT, SHIB, ATOM."
        await query.edit_message_caption(caption=text, parse_mode="Markdown")

    elif query.data == "sell_assets":
        # Запрашиваем выбор актива для продажи
        text = "💰 *Выберите актив для продажи:*\nBTC, ETH, USDT, SHIB, ATOM."
        await query.edit_message_caption(caption=text, parse_mode="Markdown")

    elif query.data == "trade_assets":
        # Обрабатываем трейд и получаем результат
        success, amount = process_trade(user_id)
        user = get_user(user_id)

        if success:
            text = (
                f"✅ *Удачный трейд!*\n\n"
                f"Вы заработали {amount}₽.\n"
                f"Ваш баланс обновлен: {user[2]}₽."
            )
        else:
            text = (
                f"❌ *Неудачный трейд!*\n\n"
                f"Вы потеряли {amount}₽.\n"
                f"Ваш баланс обновлен: {user[2]}₽."
            )

        # Создаем кнопку для возврата к активам
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⬅️ Назад", callback_data="my_assets")],
        ])

        # Обновляем сообщение с результатом трейда и кнопкой
        await query.edit_message_caption(caption=text, reply_markup=keyboard, parse_mode="Markdown")
    
    elif query.data == "withdraw":
    # Получаем данные о пользователе
        user = get_user(user_id)
        if user:
            # Формируем сообщение с запросом суммы вывода
            text = (
                f"💸 Введите сумму вывода:\n\n"
                f"У вас на балансе: {user[2]}₽\n"
                f"Минимальная сумма вывода: 1000₽"
            )

            # Добавляем инлайн-кнопку "❌ Отмена"
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Отмена", callback_data="cancel_withdrawal")]
            ])

            # Редактируем сообщение с текстом и кнопкой
            await query.edit_message_caption(
                caption=text,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

            # Сохраняем состояние "ожидание ввода суммы вывода"
            context.user_data["awaiting_withdrawal"] = True
    
    
    elif query.data == "cancel_withdrawal":
    # Отменяем вывод
        await query.edit_message_caption(
            caption="✅ Вывод отменен.",
            parse_mode="Markdown"
        )

        # Убираем состояние "ожидание ввода суммы вывода"
        if "awaiting_withdrawal" in context.user_data:
            del context.user_data["awaiting_withdrawal"]
            
    elif query.data.startswith("update_course_"):
        crypto_symbol = query.data.split("_")[-1]
        crypto_name = crypto_symbol.upper()  # Можно настроить имена для каждой монеты
        await handle_crypto_option(update, context, crypto_symbol, crypto_name)
        
    elif query.data == "cancel_crypto_option":
        await query.edit_message_text("✅ Вы вернулись к выбору опционов.")
            
    elif query.data == "option_btc":
        await handle_crypto_option(update, context, "bitcoin", "BITCOIN")
    elif query.data == "option_eth":
        await handle_crypto_option(update, context, "ethereum", "ETHEREUM")
        
    elif query.data == "verify":
        # Формируем текст сообщения для верификации
        text = (
            "🤷🏻‍♀️ К сожалению, Ваш аккаунт в данный момент не верифицирован. Рекомендуем Вам пройти верификацию аккаунта. "
            "Вы можете это сделать, нажав на кнопку ниже и написав 'Верификация' в тех. поддержку.\n\n"
            "Верифицированные аккаунты обладают рядом преимуществ над обычными. Среди них:\n\n"
            "🔷 Приоритет в очереди на выплату.\n\n"
            "🔷 Отсутствие лимитов на вывод средств.\n\n"
            "🔷 Возможность хранить средства на счету личного кабинета в разных активах.\n\n"
            "🔷 Увеличение доверия со стороны администрации и агентов технической поддержки; минимальный шанс блокировки аккаунта ввиду подозрительной активности."
        )

        # Добавляем кнопку для перехода в техническую поддержку
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Связаться с тех. поддержкой", url="https://t.me/durov")] # Поменяйте ссылку на свой аккаунт
        ])

        # Обновляем сообщение с текстом и кнопкой
        await query.edit_message_caption(caption=text, reply_markup=keyboard, parse_mode="Markdown")
        
    else:
        await query.edit_message_caption(caption="❌ Ошибка: пользователь не найден.", parse_mode="Markdown")
        
# Обработчик для кнопки с опцией "BTC"
async def handle_crypto_option(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto_symbol, crypto_name):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # Получаем текущий курс криптовалюты
    price = get_crypto_price(crypto_symbol)
    user = get_user(user_id)

    if price is not None and user:
        text = (
            f"📈 *{crypto_name} Инвестиции*\n\n"
            f"🌐 Введите сумму, которую хотите инвестировать.\n\n"
            f"Минимальная сумма инвестиций: 100₽\n"
            f"Курс {crypto_name}: {price}$\n\n"
            f"Ваш денежный баланс: {user[2]}₽"
        )

        # Создаем кнопки для обновления курса или отмены
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Обновить курс", callback_data=f"update_course_{crypto_symbol}")],
            [InlineKeyboardButton("❌ Отмена", callback_data="cancel_crypto_option")]
        ])

        # Обновляем сообщение с текстом и кнопками
        await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode="Markdown")

# Основная функция для запуска бота
if __name__ == "__main__":
    # Создаем приложение бота с использованием токена
    app = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд, текстовых сообщений и callback-запросов
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CallbackQueryHandler(get_crypto_price))
    app.add_handler(CallbackQueryHandler(handle_crypto_option))

    # Запускаем бота в режиме polling (постоянное ожидание новых сообщений)
    app.run_polling()