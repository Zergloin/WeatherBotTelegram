from telegram import Update
from telegram.ext import ContextTypes
from weather import fetch_weather_data, fetch_forecast_data
from user_settings import load_user_settings, save_user_settings
from utils import validate_date, main_menu_keyboard

user_settings = load_user_settings()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добро пожаловать! Используйте /help для получения списка команд.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Вот доступные команды:\n"
        "/weather <город> - получить погоду по названию города.\n"
        "/forecast <город> <дата> - получить прогноз погоды на указанную дату (формат: YYYY-MM-DD).\n"
        "/save_city <город> - сохранить город для дальнейшего использования.\n"
        "/get_saved_weather - получить погоду для сохраненного города.\n"
        "Отправь свое местоположение, чтобы узнать погоду в этом районе."
    )
    await update.message.reply_text(help_text, reply_markup=main_menu_keyboard())


async def weather_by_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = ' '.join(context.args)
    if not city:
        await update.message.reply_text("Пожалуйста, укажите город.")
        return
    await fetch_weather_data(update, city)


async def forecast_by_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = ' '.join(context.args[:-1])
    date = context.args[-1] if context.args else None

    if not city or (date and not validate_date(date)):
        await update.message.reply_text("Пожалуйста, используйте /forecast <город> <дата> в формате YYYY-MM-DD.")
        return

    await fetch_forecast_data(update, city, date)


async def weather_by_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_location = update.message.location
    if user_location:
        lat, lon = user_location.latitude, user_location.longitude
        await fetch_weather_data(update, None, lat, lon)
    else:
        await update.message.reply_text("Пожалуйста, отправьте свое местоположение.")


async def save_user_city(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    city = ' '.join(context.args)
    if city:
        user_settings[user_id] = city
        save_user_settings(user_settings)
        await update.message.reply_text(
            f"Город '{city}' сохранен. Используйте /get_saved_weather для получения погоды.")
    else:
        await update.message.reply_text("Пожалуйста, укажите город для сохранения.")


async def get_saved_weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    city = user_settings.get(user_id)

    if city:
        await fetch_weather_data(update, city)
    else:
        await update.message.reply_text("Вы не сохранили город. Используйте /save_city <город>, чтобы сохранить его.")


async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Извините, я не понимаю эту команду. Используйте /help для получения списка команд.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()
    response = "Спасибо за ваше сообщение! Если у вас есть вопросы, просто напишите."

    if "привет" in user_message or "здравствуй" in user_message:
        response = "Привет! Как я могу помочь вам сегодня?"
    elif "пока" in user_message or "до свидания" in user_message:
        response = "До свидания! Хорошего дня!"

    await update.message.reply_text(response)
