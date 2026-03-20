import requests
import time
import os
from datetime import datetime

BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_ID = "1403811518"  # ваш правильный Telegram ID

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": YOUR_ID, "text": text}
    try:
        requests.post(url, data=data)
        print(f"[{datetime.now()}] ✅ Отправлено")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Ошибка: {e}")

def main():
    print(f"[{datetime.now()}] 🤖 Бот запущен!")
    send_message("✅ Бот успешно запущен на сервере Bothost!")
    print("✅ Бот работает")

if __name__ == "__main__":
    main()
