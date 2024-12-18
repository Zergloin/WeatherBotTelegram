import requests
import logging
from telegram import Update
from utils import format_weather_data, format_forecast_data
from config import WEATHER_API_KEY

WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_API_URL = "http://api.openweathermap.org/data/2.5/forecast"


async def fetch_weather_data(update: Update, city: str = None, lat: float = None, lon: float = None):
    if city:
        params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
    else:
        params = {'lat': lat, 'lon': lon, 'appid': WEATHER_API_KEY, 'units': 'metric'}

    try:
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        await update.message.reply_text(format_weather_data(data))
    except requests.RequestException as ex:
        logging.error(f"Error fetching weather data: {ex}")
        await update.message.reply_text("Произошла ошибка при получении данных о погоде.")


async def fetch_forecast_data(update: Update, city: str, date: str = None):
    params = {'q': city, 'appid': WEATHER_API_KEY, 'units': 'metric'}
    try:
        response = requests.get(FORECAST_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if date:
            forecast_list = [item for item in data['list'] if item['dt_txt'].startswith(date)]
            if forecast_list:
                await update.message.reply_text(format_forecast_data({'city': data['city'], 'list': forecast_list}))
            else:
                raise requests.RequestException
        else:
            await update.message.reply_text(format_forecast_data(data))
    except requests.RequestException as ex:
        logging.error(f"Error fetching forecast data: {ex}")
        await update.message.reply_text("Произошла ошибка при получении данных о прогнозе.")
