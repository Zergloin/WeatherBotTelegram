# WeatherTelegramBot

Telegram-бот для получения текущей погоды и прогнозов по названию города или геолокации. Поддерживает сохранение города пользователя и быстрое получение погоды по нему.

## Стек

- Python 3.8+
- python-telegram-bot
- requests
- OpenWeatherMap API

## Структура

```text
weather_telegram_bot/
├── main.py               # точка входа, регистрация хендлеров
├── config.py             # API-ключи и путь к файлу настроек
├── commands.py           # обработчики команд Telegram
├── weather.py            # запросы к OpenWeatherMap и отправка ответов
├── utils.py              # форматирование сообщений, эмодзи, клавиатуры
├── user_settings.py      # сохранение/загрузка городов пользователей
├── requirements.txt      # зависимости проекта
├── user_settings.json    # файл с сохранёнными городами (создаётся автоматически)
└── README.md
```

# Данные

Бот не использует базу данных. Города, сохранённые пользователями через `/save_city`, хранятся в локальном файле `user_settings.json` в формате:

```json
{
  "user_id_1": "Moscow",
  "user_id_2": "London"
}
```

При первом запуске файл будет создан автоматически после вызова команды сохранения города.

---

# Быстрый запуск

Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/Zergloin/WeatherBotTelegram.git
cd WeatherBotTelegram
```

Создайте виртуальное окружение и установите зависимости:

```bash
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

Отредактируйте `config.py`:

- `WEATHER_API_KEY` — ключ API OpenWeatherMap (получите на https://openweathermap.org/api)
- `TELEGRAM_API_TOKEN` — токен бота, полученный от BotFather

Запустите бота:

```bash
python main.py
```

Бот начнёт опрос обновлений Telegram и будет готов к работе.

---

# Команды

| Команда | Описание |
|---|---|
| `/start` | Приветственное сообщение |
| `/help` | Список доступных команд и меню |
| `/weather <город>` | Текущая погода в указанном городе |
| `/forecast <город> <дата>` | Прогноз погоды на дату (`ГГГГ-ММ-ДД`) |
| `/save_city <город>` | Сохранить город для быстрого доступа |
| `/get_saved_weather` | Погода в сохранённом городе |
| Отправка геолокации | Текущая погода по координатам |
| Текстовые сообщения | Простые ответы на приветствия |

---

# Настройки окружения

Основные параметры задаются прямо в `config.py`:

```python
WEATHER_API_KEY = 'ваш_ключ'
TELEGRAM_API_TOKEN = 'ваш_токен'
USER_SETTINGS_FILE = 'user_settings.json'
```