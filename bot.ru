import requests
import time
import os
from datetime import datetime

# Получаем токен из переменных окружения Bothost
BOT_TOKEN = os.getenv('BOT_TOKEN')

# ВАШ Telegram ID (правильный!)
YOUR_ID = "1403811518"

def send_message(text):
    """Отправляет сообщение в Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": YOUR_ID, "text": text}
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print(f"[{datetime.now()}] ✅ Отправлено: {text[:50]}")
            return True
        else:
            print(f"[{datetime.now()}] ❌ Ошибка {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Ошибка отправки: {e}")
        return False

def main():
    """Основная функция бота"""
    print(f"[{datetime.now()}] 🤖 Бот запущен!")
    print(f"[{datetime.now()}] 🆔 Отправляю на Telegram ID: {YOUR_ID}")
    
    # Отправляем приветственное сообщение
    result = send_message("✅ Бот успешно запущен на сервере Bothost!")
    
    if result:
        print(f"[{datetime.now()}] ✅ Приветствие отправлено")
    else:
        print(f"[{datetime.now()}] ❌ Не удалось отправить приветствие")

if __name__ == "__main__":
    main()