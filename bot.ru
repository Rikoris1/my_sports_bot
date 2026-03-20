import requests
import time
import os
import json
from datetime import datetime

BOT_TOKEN = os.getenv('BOT_TOKEN')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_KEY')
YOUR_ID = "1403811518"

# Функция отправки сообщения
def send_message(text, chat_id=None):
    if chat_id is None:
        chat_id = YOUR_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=data, timeout=10)
        print(f"[{datetime.now()}] ✅ Отправлено")
        return True
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Ошибка: {e}")
        return False

# Функция получения прогнозов по шаблону
def get_predictions():
    prompt = f"""
    Ты профессиональный спортивный аналитик. Составь 5 прогнозов на {datetime.now().strftime('%d.%m.%Y')}.

    ВАЖНО:
    - Виды спорта: футбол, теннис, баскетбол
    - Букмекер: Melbet
    - Коэффициент: 1.80 – 2.10
    - Value > 5%
    - Вероятность прохода > 60%
    - ЗАПРЕЩЕНО: тоталы в футболе, ИТМ 0.5, двойной шанс с value < 10%, кэф < 1.70
    - ОЗ (обе забьют): кэф ≥ 1.6

    ОТВЕТЬ ТОЛЬКО ТАБЛИЦЕЙ В ТОЧНОМ ФОРМАТЕ (без лишнего текста):
    | № | Вид | Матч | Турнир | Ставка | Кэф | Вероятность | Value | Сумма |
    |---|------|------|--------|--------|-----|-------------|-------|-------|
    | 1 | ⚽ | Реал Мадрид - Барселона | Примера | Победа Реала | 1.85 | 65% | 7.5% | 50₽ |

    Убедись, что все матчи реальные и играются сегодня. Проверь каждый прогноз на соответствие правилам.
    """
    headers = {"Authorization": f"Bearer {DEEPSEEK_KEY}", "Content-Type": "application/json"}
    data = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}
    try:
        r = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=data, timeout=30)
        if r.status_code == 200:
            return r.json()['choices'][0]['message']['content']
        else:
            return f"❌ Ошибка API: {r.status_code}"
    except Exception as e:
        return f"❌ Ошибка соединения: {e}"

# Обработка сообщений (простая версия)
def get_updates(offset=None):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    try:
        r = requests.get(url, params=params)
        return r.json()
    except:
        return {"result": []}

# Основной цикл
def main():
    print(f"[{datetime.now()}] 🤖 Бот запущен (шаблон V5.0)")
    send_message("✅ Бот запущен! Отправь /stavka для прогнозов или жди расписания (9, 15, 20 ч).")

    last_update_id = 0
    last_sent_time = {"09:00": False, "15:00": False, "20:00": False}

    while True:
        # Обработка команд
        updates = get_updates(last_update_id + 1)
        for update in updates.get("result", []):
            last_update_id = update["update_id"]
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]
                if text == "/start":
                    send_message("Привет! Я бот с прогнозами. Отправь /stavka", chat_id)
                elif text == "/stavka" or "ставка" in text.lower():
                    send_message("📊 Генерирую прогнозы...", chat_id)
                    table = get_predictions()
                    msg = f"📊 *СТАВКИ НА {datetime.now().strftime('%d.%m.%Y')}* 📊\n\n{table}"
                    send_message(msg, chat_id)

        # Расписание
        now = datetime.now()
        current = now.strftime("%H:%M")
        if current in ["09:00", "15:00", "20:00"]:
            if not last_sent_time.get(current, False):
                print(f"[{datetime.now()}] ⏰ Расписание: {current}")
                table = get_predictions()
                msg = f"📊 *СТАВКИ НА {now.strftime('%d.%m.%Y')}* 📊\n\n{table}"
                send_message(msg)
                last_sent_time[current] = True
        else:
            for k in last_sent_time:
                last_sent_time[k] = False

        time.sleep(2)

if __name__ == "__main__":
    main()
