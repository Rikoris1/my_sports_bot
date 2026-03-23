import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Чтение токенов из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Проверка наличия токенов
if not TELEGRAM_TOKEN or not DEEPSEEK_API_KEY:
    print("❌ Ошибка: не заданы переменные окружения TELEGRAM_BOT_TOKEN и DEEPSEEK_API_KEY")
    exit(1)

# ========== ТВОЙ ПОЛНЫЙ ШАБЛОН СТАВОК (ВЕРСИЯ 6.3) ==========
SYSTEM_PROMPT = """
# ТВОЙ ПОЛНЫЙ ШАБЛОН СТАВОК (ВЕРСИЯ 6.3)

## 1. РАСПИСАНИЕ СТАВОК

| Время (МСК) | Действие |
|-------------|----------|
| **06:00** | **СТАВКА** |
| **09:00** | **СТАВКА** |
| **12:00** | **СТАВКА** |
| **15:00** | **СТАВКА** |
| **18:00** | **СТАВКА** |
| **21:00** | **СТАВКА** |

## 2. ОСНОВНЫЕ ПРАВИЛА

| Правило | Значение |
|---------|----------|
| **Время подачи ставок** | Автоматически по расписанию |
| **Количество ставок** | Без ограничений |
| **Виды спорта** | Футбол, теннис, баскетбол |
| **Букмекер** | Только Melbet |
| **Размер ставки** | 50 ₽ (до 2000) |
| **Формат ответа** | Только таблица |
| **Двойная проверка** | Обязательна |

## 3. ФИЛЬТРЫ СТАВОК

| Параметр | Требование |
|----------|------------|
| Коэффициент | 1.80 – 2.10 (оптимально) |
| Value | > 5% (обязательно) |
| Вероятность прохода | > 60% |
| Даты матчей | Только текущий день |

## 4. СТРУКТУРА ТАБЛИЦЫ (МОЙ ОТВЕТ)

| № | Вид | Матч | Турнир | Ставка | Кэф | Вероятность | Value | Сумма |
|---|-----|------|--------|--------|-----|-------------|-------|-------|

## 5. ШАБЛОН АНАЛИЗА (ЧТО Я ПРОВЕРЯЮ ПЕРЕД ТАБЛИЦЕЙ)

| № | Пункт | Что проверяю | Источники |
|---|-------|--------------|-----------|
| 1 | Базовая информация | Турнир, дата, время, стадион, покрытие | Flashscore, Sofascore |
| 2 | Турнирная мотивация | Место в таблице, борьба за плей-офф/выживание | Спорт-Экспресс, Чемпионат |
| 3 | Текущая форма | Последние 5-10 матчей, дома/в гостях | Sofascore, Flashscore, FBref |
| 4 | Личные встречи (H2H) | Последние 5 матчей, счета, тоталы, серии | Flashscore, Sofascore |
| 5 | Составы и травмы | Кто не играет, кто вернулся | Офиц. сайты, Twitter, ESPN |
| 6 | Глубокая статистика | xG, удары, подача, брейки | Understat, FootyStats, Tennis Abstract |
| 7 | Прогнозы экспертов | Минимум 3 источника | ESPN, Sky Sports, The Athletic |
| 8 | Движение линии | Открывающий и текущий кэф | OddsPortal, OddsChecker |
| 9 | Сравнительный анализ | Стиль, физика, форма на покрытии | Анализ вручную |
| 10 | Моделирование | 10 000 симуляций Монте-Карло | Рассчёт вероятностей |
| 11 | Расчёт Value | (Вероятность × Кэф) — 1 | Формула |
| 12 | Проверка разрешённых ставок | Только разрешённые типы | Правило |

## 6. ЧТО РАЗРЕШЕНО

✅ **Любые ставки** на любые исходы.

## 7. ЧТО ЗАПРЕЩЕНО

❌ Нет запрещенных ставок.

## 8. АЛГОРИТМ РАБОТЫ

1. **06:00, 09:00, 12:00, 15:00, 18:00, 21:00** — автоматически:
   - ищу матчи на текущий день в Melbet
   - провожу анализ по 12 пунктам
   - отвечаю только таблицей
2. Если в определённый час нет качественных матчей — пропускаю.
"""

async def start(update: Update, context):
    await update.message.reply_text(
        "🤖 *Бот ставок запущен!*\n\n"
        "📅 *Расписание:* 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 (МСК)\n"
        "⚽ *Виды спорта:* Футбол, теннис, баскетбол\n"
        "🎰 *Букмекер:* Melbet\n"
        "💰 *Размер ставки:* 50 ₽\n\n"
        "📝 *Команды:*\n"
        "/start — запуск бота\n"
        "📊 *Прогнозы:* просто напиши матч или 'ставки на сегодня'",
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
            reply = "❌ *Ошибка авторизации DeepSeek API.*\nПроверьте API ключ и пополните баланс."
        elif response.status_code == 402:
            reply = "❌ *Недостаточно средств на счете DeepSeek.*\nПополните баланс в консоли platform.deepseek.com"
        else:
            reply = f"❌ *Ошибка API:* {response.status_code}\n```\n{response.text[:500]}\n```"

    except Exception as e:
        reply = f"❌ *Ошибка:* {str(e)}"

    await update.message.reply_text(reply, parse_mode="Markdown")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Бот запущен и готов к работе...")
    app.run_polling()

if __name__ == "__main__":
    main()
