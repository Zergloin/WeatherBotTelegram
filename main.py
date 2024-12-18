import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from commands import start_command, help_command, weather_by_city, forecast_by_city, save_user_city, get_saved_weather, \
    weather_by_location, handle_message, unknown_command
from config import TELEGRAM_API_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("weather", weather_by_city))
    application.add_handler(CommandHandler("forecast", forecast_by_city))
    application.add_handler(CommandHandler("save_city", save_user_city))
    application.add_handler(CommandHandler("get_saved_weather", get_saved_weather))
    application.add_handler(MessageHandler(filters.LOCATION, weather_by_location))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    application.run_polling()


if __name__ == '__main__':
    main()
