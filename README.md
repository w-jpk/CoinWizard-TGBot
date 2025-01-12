# CoinWizard Telegram Bot

Этот проект представляет собой Telegram-бота, который помогает пользователям управлять своим виртуальным балансом, проводить трейды и взаимодействовать с криптовалютными опционами. Бот создан для демонстрации возможностей Telegram API и использования базы данных SQLite для хранения информации о пользователях.

## Оглавление

- [Предупреждение](#важное-предупреждение)
- [Установка и настройка](#установка-и-настройка)
- [Создание файла config.py](#создание-файла-configpy)
- [Запуск бота](#запуск-бота)
- [Функционал бота](#функционал-бота)
- [Структура проекта](#структура-проекта)
- [Обновления](#обноваления)

## Важное предупреждение

Этот бот создан исключительно в **развлекательных и поучительных целях**. Он не предназначен для использования в реальных финансовых операциях или торговле. Все данные, включая баланс, операции и результаты трейдов, являются виртуальными и не имеют отношения к реальным деньгам или активам.

Разработчики и создатели бота **не несут никакой ответственности** за любые действия, предпринятые пользователями на основе информации, предоставленной ботом. Использование бота осуществляется на ваш собственный риск.

Если вы хотите заниматься реальной торговлей или инвестициями, обратитесь к лицензированным финансовым учреждениям и консультантам.

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
```

### Пример:

```python
# config.py
BOT_TOKEN = "1234567890:ABCdefGhIJKlmNoPQRstuVWXyz"
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

### 12.01.2025

1. Бот добавлен на GitHub
2. Добавлено:
  - Функционал криптовалют;
  - Сообщение верификации.
