# CoinWizard Telegram Bot

Этот проект представляет собой Telegram-бота, который помогает пользователям управлять своим виртуальным балансом, проводить трейды и взаимодействовать с криптовалютными опционами. Бот создан для демонстрации возможностей Telegram API и использования базы данных SQLite для хранения информации о пользователях.

## Оглавление

- [Предупреждение](#важное-предупреждение)
- [Установка и настройка](#установка-и-настройка)
- [Создание файла config.py](#создание-файла-configpy)
- [Запуск бота](#запуск-бота)
- [Функционал бота](#функционал-бота)
- [Структура проекта](#структура-проекта)
- [Обновления](#обновления)

## Важное предупреждение

Этот бот создан исключительно в **развлекательных и поучительных целях**. Он не предназначен для использования в реальных финансовых операциях или торговле. Все данные, включая баланс, операции и результаты трейдов, являются виртуальными и не имеют отношения к реальным деньгам или активам.

Разработчики и создатели бота **не несут никакой ответственности** за любые действия, предпринятые пользователями на основе информации, предоставленной ботом. Использование бота осуществляется на ваш собственный риск.

Если вы хотите заниматься реальной торговлей или инвестициями, обратитесь к лицензированным финансовым учреждениям и консультантам.

---

⚠️ **Важно!** Если вы увидели похожего бота, который требует перевести реальные деньги или обещает гарантированную прибыль, не доверяйте таким предложениям! Это может быть мошенничество. Никогда не переводите деньги незнакомым лицам и не доверяйте сомнительным источникам. Будьте бдительны и сохраняйте осторожность!

## Установка и настройка

### 1. Клонируйте репозиторий

Для начала работы с проектом склонируйте репозиторий на ваш компьютер:

```bash
git clone https://github.com/w-jpk/CoinWizard-TGBot.git
cd CoinWizard_TGBot
```

## Создание файла config.py

Для работы бота требуется токен, который вы получаете при создании бота через BotFather в Telegram.

1. Создайте файл config.py в корневой директории проекта.
2. Добавьте в него следующую строку, заменив "ВАШ ТОКЕН БОТА" на ваш токен:

```python
# config.py
BOT_TOKEN = "ВАШ ТОКЕН БОТА"
adm = ВАШ ID
check = ID чата куда будут приходить чеки
card = "ваши реквизиты"
```

### Пример:

```python
# config.py
BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRstuVWXyz"
amd = [12345, 67890] - можно добавлять несколько администраторов
check = -123456789 - чат куда приходят уведомления
card = "4100 1234 5678 9012" - реквизит для перевода
```

### Важно: Никогда не делитесь вашим токеном публично и не добавляйте его в репозиторий. Убедитесь, что файл config.py добавлен в .gitignore, чтобы избежать случайной утечки токена.

## Запуск бота

После настройки файла config.py вы можете запустить бота:

```bash
python bot.py
```

Бот начнет работать и будет отвечать на команды и сообщения в Telegram.

## Функционал бота

Бот предоставляет следующие возможности:

- Личный кабинет:
  - Просмотр баланса.
  - Просмотр статистики (количество успешных и неудачных операций, выводы и т.д.).
  - Пополнение баланса (виртуальное).
  - Вывод средств (виртуальный).
- Опционы:
  - Возможность "инвестировать" в криптовалюты (BTC, ETH, BNB и другие).
  - Симуляция трейдов с вероятностью успеха 50%.
- Техническая поддержка:
  - Ссылка на чат с поддержкой.
- Информация о сервисе:
  - Краткое описание возможностей бота.

## Структура проекта

```plaintext
CoinWizard_TGBot/
├── bot.py                # Основной файл бота
├── database.py           # Файл для работы с базой данных SQLite
├── config.py             # Файл для хранения токена бота (создается вручную)
├── README.md             # Документация проекта
└── assets/               # Папка для хранения изображений и других ресурсов
    └── project-1.jpg     # Пример изображения для личного кабинета
```

## Обновления

- ### 12.01.2025

  - Бот добавлен на GitHub;
  - Добавлено:

    - Функционал криптовалют;
    - Сообщение "🗃 Верификация";
    - Сообщение "🔷 О сервисе";
    - Сообщение "📜 Сертификат";
    - Сообщение "Гарантия сервиса";
    - Сообщение "📈 Состояние сети".

  - Обновлена ссылка на чат в следующих местах:

  ```
  elif text == "🧑🏻‍💻 Тех.Поддержка":
    ...остальная часть кода...
    [InlineKeyboardButton("📩 Написать", url="https://t.me/durov")] # Поменяйте ссылку на свой аккаунт

  elif query.data == "verify":
    ...остальная часть кода...
    [InlineKeyboardButton("💬 Связаться с тех. поддержкой", url="https://t.me/durov")] # Поменяйте ссылку на свой аккаунт
  ```

- ### 18.01.2025

  - Обновлен функционал пополнения по карте. Теперь можно вводить и пополнять любую сумму.

- ### 19.01.2025

  - Добавлен функционал игры(Опционы -> Выбрать опцион -> Ввести сумму -> Выбрать направление графика -> Выбрать время -> Ожидать результат);
  - Добавлен пункт верификации в БД;
  - Внесены изменения в код;
  - Добавлены команды для администатора:
  ```
  /add_balance ID пользователя сумма - команда для пополнения баланса пользователю.
  Пример: /add_balance 123456789 10000

  /verify_user ID пользователя 0 или 1 - команда для верификации пользователя.
  Пример: /verify_user 123456789 1

  /set_balance ID пользователя сумма - команда для установки определенного баланса пользователю.
  Пример: /set_balance 123456789 10000

  /withdraw_funds ID пользователя сумма - команда для вывода средств пользователя.
  Пример: /withdraw_funds 123456789 10000

  /broadcast сообщение - команда для отправки объявления всем пользователям.
  Пример: /broadcast важное сообщение!

  /user_info ID пользователя - команда для получения данных пользователя.
  Пример: /user_info 123456789
  ```
  - Добавлен новый метод пополнения. Теперь пополнение происходит через подтверждение администратором. Как это работат: Пользователь выбирает пополнить через банковскую карту -> Бот отправляет ему реквезиты и ожидает скриншот чека -> После получения чека бот отправляет это сообщение администратору и администратор проверяет чек, после чего при помощи команды /add_balance пополняет счет пользователю.

  - Добавлен новый метод вывода;
  - Добавлена система промокодов: PROMO100, PROMO500, PROMO1000;
  - Добавлена проверка верификации для вывода средств;
  - Обновлен запрос на верификацию;
  - Добавлена команда /help для администрации;
  - Изменен механизм обращения в тех. поддержку.

- ### 20.01.2025

  - Добавлена реферальная система: перешедший пользователь получает 1.000₽, создатель рефки получает 5.000₽;
  - Перенес реквизиты в файл config.py, теперь файл выглядит так:
  ```
  # config.py
  BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRstuVWXyz"
  amd = [12345, 67890] - можно добавлять несколько администраторов
  check = -123456789 - чат куда приходят уведомления
  card = "4100 1234 5678 9012" - реквизит для перевода
  ```
  - Обновлено [Предупреждение](#важное-предупреждение).