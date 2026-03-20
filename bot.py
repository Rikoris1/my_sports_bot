import requests
import time
import os
from datetime import datetime

BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_ID = "127801716"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": YOUR_ID, "text": text}
    try:
        requests.post(url, data=data)
        print(f"[{datetime.now()}] ✅ Отправлено")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Ошибка: {e}")

def main():
    send_message("✅ Бот запущен!")
    print("✅ Бот работает")

if __name__ == "__main__":
    main()