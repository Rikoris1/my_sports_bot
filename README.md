# 🤖 Sports Betting Bot

Telegram-бот для спортивных прогнозов на базе DeepSeek AI.

## 📋 Функции
- Анализ матчей по 12 параметрам
- Прогнозы на футбол, теннис, баскетбол
- Букмекер: Melbet
- Формат ответа: таблица

## 📅 Расписание ставок
06:00, 09:00, 12:00, 15:00, 18:00, 21:00 (МСК)

## 🚀 Запуск

### Локально
```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Создать файл .env с токенами
TELEGRAM_BOT_TOKEN=
8746367957:AAFjebamcyRUDNEfA_eJamv1gKQ4-iLXS2Qн
DEEPSEEK_API_KEY=sk-dacc289dcf5641f58478786eeb00ca11

# 3. Запустить бота
python bot.py
