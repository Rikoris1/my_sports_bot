import requests
import time
import os
import json
from datetime import datetime

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_KEY')
YOUR_ID = "1403811518"

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": YOUR_ID, "text": text, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=data, timeout=10)
        print(f"[{datetime.now()}] ✅ Отправлено")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Ошибка: {e}")

def get_predictions():
    """Запрашивает прогнозы по вашему шаблону"""
    prompt = f"""
    Ты профессиональный спортивный аналитик. Составь 5 прогнозов на {datetime.now().strftime('%d.%m.%Y')}.

    ТВОЙ ШАБЛОН:
    - Виды спорта: футбол, теннис, баскетбол
    - Букмекер: Melbet
    - Коэффициент: 1.80 – 2.10
    - Value > 5%
    - Вероятность прохода > 60%
    - Запрещено: тоталы в футболе, ИТМ 0.5, двойной шанс с value < 10%, кэф < 1.70
    - ОЗ (обе забьют): кэф ≥ 1.6

    ОТВЕТЬ ТОЛЬКО ТАБЛИЦЕЙ В ФОРМАТЕ:
    | № | Вид | Матч | Турнир | Ставка | Кэф | Вероятность | Value | Сумма |
    |---|------|------|--------|--------|-----|-------------|-------|-------|
    | 1 | ⚽ | Команда1 - Команда2 | Лига | Победа Команды1 | 1.85 | 65% | 7.5% | 50₽ |

    Убедись, что все матчи реальные и играются сегодня.
    """
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
    try:
        r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content']
        else:
            return f"❌ Ошибка API DeepSeek: {r.status_code}"
    except Exception as e:
        return f"❌ Ошибка соединения: {e}"

def main():
    print(f"[{datetime.now()}] 🤖 Бот запущен по шаблону V5.0")
    send_message("✅ Бот с прогнозами запущен! Отправьте команду /stavka или ждите расписания.")

    while True:
        now = datetime.now()
        current = now.strftime("%H:%M")
        if current in ["09:00", "15:00", "20:00"]:
            print(f"[{datetime.now()}] ⏰ Генерация прогнозов...")
            table = get_predictions()
            msg = f"📊 *СТАВКИ НА {now.strftime('%d.%m.%Y')}* 📊\n\n{table}"
            send_message(msg)
            time.sleep(61)
        time.sleep(30)

if __name__ == "__main__":
    main()
