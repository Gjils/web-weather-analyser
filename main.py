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
                    "lang": "ru"
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None