import uuid
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
import os

app = Flask(__name__)
app.secret_key = uuid.uuid4().hex

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


weather_api = WeatherAPI(API_KEY)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        start_city = request.form.get("start_city")
        end_city = request.form.get("end_city")

        if not start_city or not end_city:
            flash("Пожалуйста, заполните оба поля!")
            return redirect(url_for("index"))

        start_weather = weather_api.get_weather(start_city)
        end_weather = weather_api.get_weather(end_city)

        if start_weather is None or end_weather is None:
            flash("Не удалось получить данные о погоде. Проверьте введённые города.")
            return redirect(url_for("index"))

        start_weather_bad = is_bad_weather(start_weather)
        end_weather_bad = is_bad_weather(end_weather)

        return render_template(
            "result.html",
            start_city=start_city,
            end_city=end_city,
            start_weather=start_weather,
            end_weather=end_weather,
            start_weather_bad=start_weather_bad,
            end_weather_bad=end_weather_bad,
        )

    return render_template("index.html")


def main():
    app.run(debug=True, host="0.0.0.0", port=5555)


if __name__ == "__main__":
    main()
