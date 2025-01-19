# database.py

# Импортируем модуль для работы с SQLite
import sqlite3

# Импортируем модуль для генерации случайных чисел
import random

# Функция для инициализации базы данных
def init_db():
    # Устанавливаем соединение с базой данных (если файл bot.db не существует, он будет создан)
    conn = sqlite3.connect("bot.db")
    
    # Создаем курсор для выполнения SQL-запросов
    cursor = conn.cursor()
    
    # Создаем таблицу users, если она еще не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,         
            username TEXT,
            balance REAL DEFAULT 0,          
            operations_count INTEGER DEFAULT 0,  
            successful_operations INTEGER DEFAULT 0, 
            failed_operations INTEGER DEFAULT 0,  
            conclusions INTEGER DEFAULT 0,  
            total_withdrawn REAL DEFAULT 0,
            verif BOOLEN DEFAULT false,
            referral_status BOOLEN DEFAULT false
        )
    ''')
    
    # Фиксируем изменения в базе данных
    conn.commit()
    
    # Закрываем соединение с базой данных
    conn.close()

# Функция для добавления нового пользователя в базу данных
def add_user(user_id, username):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    # Вставляем нового пользователя в таблицу users, если он еще не существует
    # Используем INSERT OR IGNORE, чтобы избежать дублирования записей
    cursor.execute('''
        INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)
    ''', (user_id, username))
    
    # Фиксируем изменения в базе данных
    conn.commit()
    
    # Закрываем соединение с базой данных
    conn.close()

def dep_balance(user_id, amount):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    # Обновляем баланс пользователя, увеличиваем счетчик операций и успешных операций
    cursor.execute('''
        UPDATE users 
        SET balance = balance + ?
        WHERE id = ?
    ''', (amount, user_id))
    
    # Фиксируем изменения в базе данных
    conn.commit()
    
    # Закрываем соединение с базой данных
    conn.close() 

# Функция для обновления баланса пользователя
def update_balance(user_id, amount):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    # Обновляем баланс пользователя, увеличиваем счетчик операций и успешных операций
    cursor.execute('''
        UPDATE users 
        SET balance = balance + ?, 
            operations_count = operations_count + 1, 
            successful_operations = successful_operations + 1 
        WHERE id = ?
    ''', (amount, user_id))
    
    # Фиксируем изменения в базе данных
    conn.commit()
    
    # Закрываем соединение с базой данных
    conn.close()

def win(user_id, amount):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET balance = balance + ?, 
            operations_count = operations_count + 1, 
            successful_operations = successful_operations + 1 
        WHERE id = ?
    ''', (amount, user_id))
    
    conn.commit()
    
    conn.close()

def lose(user_id, amount):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET balance = balance - ?, 
            operations_count = operations_count + 1, 
            failed_operations = failed_operations + 1 
        WHERE id = ?
    ''', (amount, user_id))
    
    conn.commit()
    
    conn.close()

# Функция для получения информации о пользователе по его ID
def get_user(user_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    # Выполняем запрос для получения данных о пользователе
    cursor.execute('''
        SELECT * FROM users WHERE id = ?
    ''', (user_id,))
    
    # Получаем первую запись из результата запроса
    user = cursor.fetchone()
    
    # Закрываем соединение с базой данных
    conn.close()
    
    # Возвращаем данные о пользователе
    return user

# Функция для обработки трейда (покупки/продажи активов)
def process_trade(user_id):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    # Задаем вероятность успешного трейда (50%)
    success_chance = 0.5
    
    # Генерируем случайное число и проверяем, успешен ли трейд
    is_successful = random.random() < success_chance 

    if is_successful:
        # Если трейд успешен, генерируем случайную прибыль
        profit = random.randint(10000, 50000)
        
        # Обновляем баланс пользователя, увеличиваем счетчик успешных операций и общий счетчик операций
        cursor.execute('''
            UPDATE users
            SET balance = balance + ?, 
                successful_operations = successful_operations + 1, 
                operations_count = operations_count + 1
            WHERE id = ?
        ''', (profit, user_id))
        
        # Фиксируем изменения в базе данных
        conn.commit()
        
        # Закрываем соединение с базой данных
        conn.close()
        
        # Возвращаем результат: успех и сумму прибыли
        return True, profit 
    else:
        # Если трейд неудачен, генерируем случайный убыток
        loss = random.randint(5000, 25000)
        
        # Обновляем баланс пользователя, увеличиваем счетчик неудачных операций и общий счетчик операций
        cursor.execute('''
            UPDATE users
            SET balance = balance - ?, 
                failed_operations = failed_operations + 1, 
                operations_count = operations_count + 1
            WHERE id = ?
        ''', (loss, user_id))
        
        # Фиксируем изменения в базе данных
        conn.commit()
        
        # Закрываем соединение с базой данных
        conn.close()
        
        # Возвращаем результат: неудача и сумму убытка
        return False, loss
    
def withdraw_funds(user_id, amount):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()

    # Проверяем, достаточно ли средств на балансе
    cursor.execute('''
        SELECT balance FROM users WHERE id = ?
    ''', (user_id,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        # Обновляем баланс, увеличиваем счетчик выводов и общую сумму выводов
        cursor.execute('''
            UPDATE users
            SET balance = balance - ?,
                conclusions = conclusions + 1,
                total_withdrawn = total_withdrawn + ?
            WHERE id = ?
        ''', (amount, amount, user_id))
        conn.commit()
        conn.close()
        return True  # Успешный вывод
    else:
        conn.close()
        return False  # Недостаточно средств
    
def update_user_referral_status(user_id, bool):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    
    # Обновляем баланс пользователя, увеличиваем счетчик операций и успешных операций
    cursor.execute('''
        UPDATE users 
        SET referral_status = ?
        WHERE id = ?
    ''', (bool, user_id))
    
    # Фиксируем изменения в базе данных
    conn.commit()
    
    # Закрываем соединение с базой данных
    conn.close() 