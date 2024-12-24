import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from flask import Flask
import requests
import pandas as pd
import plotly.graph_objects as go
import folium
from folium.plugins import MarkerCluster
import os

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

API_KEY = os.getenv("OPEN_WEATHER_KEY")
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/direct"


def get_coordinates(city_name):
    try:
        response = requests.get(
            GEOCODE_URL, params={"q": city_name, "appid": API_KEY, "limit": 1}
        )
        response.raise_for_status()
        data = response.json()
        if data:
            return data[0]["lat"], data[0]["lon"]
    except requests.exceptions.RequestException:
        return None, None


def get_forecast(city_name):
    lat, lon = get_coordinates(city_name)
    if lat is None or lon is None:
        return None
    try:
        response = requests.get(
            BASE_URL_FORECAST,
            params={
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric",
                "lang": "ru",
            },
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


def create_weather_graph(data, city_name, indicators):
    df = pd.DataFrame(
        [
            {
                "Дата": item["dt_txt"],
                "Температура (°C)": item["main"]["temp"],
                "Скорость ветра (м/с)": item["wind"]["speed"],
                "Осадки (мм)": item.get("rain", {}).get("3h", 0)
                + item.get("snow", {}).get("3h", 0),
            }
            for item in data["list"]
        ]
    )

    fig = go.Figure()

    if "Температура" in indicators:
        fig.add_trace(
            go.Scatter(
                x=df["Дата"],
                y=df["Температура (°C)"],
                mode="lines+markers",
                name="Температура",
                line=dict(color="red"),
            )
        )

    if "Скорость ветра" in indicators:
        fig.add_trace(
            go.Scatter(
                x=df["Дата"],
                y=df["Скорость ветра (м/с)"],
                mode="lines+markers",
                name="Скорость ветра",
                line=dict(color="blue"),
            )
        )

    if "Осадки" in indicators:
        fig.add_trace(
            go.Bar(
                x=df["Дата"],
                y=df["Осадки (мм)"],
                name="Осадки",
                marker=dict(color="green"),
            )
        )

    fig.update_layout(
        title=f"Прогноз погоды для {city_name}",
        xaxis_title="Дата",
        yaxis_title="Значение",
        barmode="group",
        template="plotly_white",
        legend_title="Показатели",
    )

    return fig


def create_weather_map_with_route(cities):
    if not cities:
        return None

    coordinates = [get_coordinates(city) for city in cities]
    valid_coordinates = [
        (lat, lon) for lat, lon in coordinates if lat is not None and lon is not None
    ]

    if not valid_coordinates:
        return None

    map_center = valid_coordinates[0]
    weather_map = folium.Map(location=map_center, zoom_start=6)
    marker_cluster = MarkerCluster().add_to(weather_map)

    for city, (lat, lon) in zip(cities, valid_coordinates):
        forecast = get_forecast(city)
        if forecast:
            temp = forecast["list"][0]["main"]["temp"]
            weather = forecast["list"][0]["weather"][0]["description"]
            popup_text = f"<b>{city}</b><br>Температура: {temp}°C<br>Погода: {weather}"
            folium.Marker(location=(lat, lon), popup=popup_text).add_to(marker_cluster)

    folium.PolyLine(
        locations=valid_coordinates,
        color="blue",
        weight=4,
        opacity=0.8,
        popup="Маршрут",
    ).add_to(weather_map)

    map_path = "temp_map.html"
    weather_map.save(map_path)
    return map_path


app.layout = html.Div(
    [
        html.H1("Прогноз погоды и маршрут", style={"textAlign": "center"}),
        html.Div(
            [
                html.Label("Введите начальный город:"),
                dcc.Input(
                    id="start-city",
                    type="text",
                    placeholder="Начальный город",
                    debounce=True,
                ),
            ],
            style={"padding": "10px"},
        ),
        html.Div(
            [
                html.Label("Введите конечный город:"),
                dcc.Input(
                    id="end-city",
                    type="text",
                    placeholder="Конечный город",
                    debounce=True,
                ),
            ],
            style={"padding": "10px"},
        ),
        html.Div(
            [
                html.Label("Введите промежуточные города (через запятую):"),
                dcc.Input(
                    id="intermediate-cities",
                    type="text",
                    placeholder="Город1, Город2,...",
                    debounce=True,
                ),
            ],
            style={"padding": "10px"},
        ),
        html.Div(
            [
                html.Label("Выберите город для отображения на графике:"),
                dcc.Dropdown(
                    id="city-dropdown", options=[], value=None, clearable=False
                ),
            ],
            style={"padding": "20px"},
        ),
        html.Div(
            [
                html.Label("Выберите показатели для отображения на графике:"),
                dcc.Checklist(
                    id="indicators",
                    options=[
                        {"label": "Температура", "value": "Температура"},
                        {"label": "Скорость ветра", "value": "Скорость ветра"},
                        {"label": "Осадки", "value": "Осадки"},
                    ],
                    value=["Температура", "Скорость ветра", "Осадки"],
                    inline=True,
                ),
            ],
            style={"padding": "20px"},
        ),
        dcc.Loading(
            type="circle",
            children=[
                dcc.Graph(id="weather-graph"),
            ],
            style={"padding": "20px"},
        ),
        dcc.Loading(
            type="circle",
            children=[
                html.Div(
                    [
                        html.Label("Карта маршрута:"),
                        html.Iframe(
                            id="weather-map",
                            style={
                                "width": "100%",
                                "height": "600px",
                                "border": "none",
                            },
                        ),
                    ],
                    style={"padding": "20px"},
                ),
            ],
            style={"padding": "20px"},
        ),
    ]
)


@app.callback(
    [
        Output("city-dropdown", "options"),
        Output("weather-graph", "figure"),
        Output("weather-map", "srcDoc"),
    ],
    [
        Input("start-city", "value"),
        Input("end-city", "value"),
        Input("intermediate-cities", "value"),
        Input("city-dropdown", "value"),
        Input("indicators", "value"),
    ],
)
def update_visualizations(
    start_city, end_city, intermediate_cities, selected_city, indicators
):
    cities = []
    if start_city:
        cities.append(start_city)
    if intermediate_cities:
        cities += [
            city.strip() for city in intermediate_cities.split(",") if city.strip()
        ]
    if end_city:
        cities.append(end_city)

    if not cities:
        return [], go.Figure().update_layout(title="Введите хотя бы один город"), None

    dropdown_options = [{"label": city, "value": city} for city in cities]

    selected_city = selected_city or cities[0]

    forecast_data = get_forecast(selected_city)
    if not forecast_data:
        return (
            dropdown_options,
            go.Figure().update_layout(title="Не удалось получить данные"),
            None,
        )

    weather_graph = create_weather_graph(forecast_data, selected_city, indicators)

    map_path = create_weather_map_with_route(cities)
    with open(map_path, "r", encoding="utf-8") as f:
        map_html = f.read()
    os.remove(map_path)

    return dropdown_options, weather_graph, map_html


if __name__ == "__main__":
    app.run_server(debug=True)
