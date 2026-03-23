import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not TELEGRAM_TOKEN or not DEEPSEEK_API_KEY:
    print("❌ Ошибка: не заданы переменные окружения")
    exit(1)

SYSTEM_PROMPT = """
# ТВОЙ ПОЛНЫЙ ШАБЛОН СТАВОК (ВЕРСИЯ 6.3)

## 1. РАСПИСАНИЕ СТАВОК
| Время (МСК) | Действие |
|-------------|----------|
| 06:00 | СТАВКА |
| 09:00 | СТАВКА |
| 12:00 | СТАВКА |
| 15:00 | СТАВКА |
| 18:00 | СТАВКА |
| 21:00 | СТАВКА |

## 2. ОСНОВНЫЕ ПРАВИЛА
| Правило | Значение |
|---------|----------|
| Виды спорта | Футбол, теннис, баскетбол |
| Букмекер | Melbet |
| Размер ставки | 50 ₽ |
| Формат ответа | Только таблица |

## 3. СТРУКТУРА ТАБЛИЦЫ
| № | Вид | Матч | Турнир | Ставка | Кэф | Вероятность | Value | Сумма |

## 4. ЧТО ЗАПРЕЩЕНО
- ❌ Тотал меньше 0.5
"""

async def start(update: Update, context):
    await update.message.reply_text(
        "🤖 *Бот ставок запущен!*\n\n"
        "📅 *Расписание:* 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 (МСК)\n"
        "⚽ *Виды спорта:* Футбол, теннис, баскетбол\n"
        "🎰 *Букмекер:* Melbet\n\n"
        "📊 *Прогнозы:* напиши 'ставки на сегодня'",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context):
    user_message = update.message.text

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Сейчас {datetime.now().strftime('%H:%M')} МСК. {user_message}"}
    ]

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": 0.3
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=45
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        elif response.status_code == 401:
            reply = "❌ Ошибка авторизации DeepSeek API. Проверьте API ключ."
        elif response.status_code == 402:
            reply = "❌ Недостаточно средств на счете DeepSeek. Пополните баланс."
        else:
            reply = f"❌ Ошибка API: {response.status_code}"

    except Exception as e:
        reply = f"❌ Ошибка: {str(e)}"

    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен и готов к работе...")
    app.run_polling()

if __name__ == "__main__":
    main()
