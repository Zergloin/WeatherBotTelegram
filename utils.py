import datetime
from telegram import ReplyKeyboardMarkup


def validate_date(date_str):
    try:
        year, month, day = map(int, date_str.split('-'))
        datetime.date(year, month, day)
        return True
    except ValueError:
        return False


def format_weather_data(data):
    city_name = data['name']
    weather_description = data['weather'][0]['description']
    temperature = data['main']['temp']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    emoji = get_weather_emoji(weather_description)
    weather_description_ru = translate_weather_description(weather_description)

    return (
        f"🌍 *Погода в {city_name}* 🌍\n"
        f"☁️ *Описание:* {weather_description_ru}\n"
        f"🌡️ *Температура:* {temperature:.2f}°C\n"
        f"💧 *Влажность:* {humidity}%\n"
        f"💨 *Скорость ветра:* {wind_speed:.2f} м/с\n"
        f"{emoji}"
    )


def format_forecast_data(data):
    city_name = data['city']['name']
    forecast_info = f"🌍 *Прогноз погоды для {city_name}* 🌍\n"

    for item in data['list']:
        date_time = item['dt_txt']
        weather_description = item['weather'][0]['description']
        temperature = item['main']['temp']
        humidity = item['main']['humidity']
        wind_speed = item['wind']['speed']
        emoji = get_weather_emoji(weather_description)
        weather_description_ru = translate_weather_description(weather_description)

        forecast_info += (
            f"\n📅 *Дата и время:* {date_time}\n"
            f"☁️ *Описание:* {weather_description_ru} {emoji}\n"
            f"🌡️ *Температура:* {temperature:.2f}°C\n"
            f"💧 *Влажность:* {humidity}%\n"
            f"💨 *Скорость ветра:* {wind_speed:.2f} м/с\n"
            f"{emoji}"
        )

    return forecast_info


def translate_weather_description(description):
    translations = {
        "clear sky": "ясное небо",
        "few clouds": "немного облаков",
        "scattered clouds": "разрозненные облака",
        "broken clouds": "облачность",
        "shower rain": "дождь",
        "rain": "дождь",
        "thunderstorm": "гроза",
        "snow": "снег",
        "mist": "туман",
        "light rain": "небольшой дождь",
        "light snow": "небольшой снег",
        "overcast clouds": "пасмурные облака"
    }
    return translations.get(description, description)


def get_weather_emoji(description):
    if "clear" in description:
        return "☀️"
    elif "cloud" in description:
        return "☁️"
    elif "rain" in description:
        return "🌧️"
    elif "snow" in description:
        return "❄️"
    elif "storm" in description:
        return "⛈️"
    return ""


def main_menu_keyboard():
    keyboard = [
        ["/get_saved_weather"],
        ["/help"]
    ]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
