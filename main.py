import requests
import os

# АссгWeather не работал, решил использовать OpenWeather
API_KEY = os.getenv("OPEN_WEATHER_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_weather(self, city_name):
        try:
            response = requests.get(
                BASE_URL,
                params={
                    "q": city_name,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "ru",
                },
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None


def is_bad_weather(data):
    try:
        temperature = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        precipitation = max(
            data.get("rain", {}).get("1h", 0), data.get("snow", {}).get("1h", 0)
        )
        clouds = data["clouds"]["all"]
        return (
            temperature < 0
            or temperature > 35
            or wind_speed > 10
            or precipitation > 2
            or clouds > 80
        )
    except KeyError:
        return False
