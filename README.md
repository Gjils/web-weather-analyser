# Прогноз погоды и маршрут

Это веб-приложение для отображения прогноза погоды на основе данных OpenWeather API. Пользователи могут вводить начальный, конечный и промежуточные города маршрута, а также выбирать, какие погодные параметры (температура, скорость ветра, осадки) они хотят видеть на графике.

Приложение также позволяет отображать маршрут на интерактивной карте с прогнозами погоды для каждого города на маршруте.

## Функциональность
-	Ввод начального, конечного и промежуточных городов маршрута.
-	Выбор параметров для отображения на графиках (температура, скорость ветра, осадки).
-	Визуализация прогноза погоды на графиках с использованием Plotly.
-	Отображение интерактивной карты маршрута с линией маршрута и маркерами для каждого города.
-	Индикация загрузки при получении данных.

## Технологии
-	Python — основной язык программирования.
-	Dash — фреймворк для создания веб-приложений с использованием Python.
-	Plotly — библиотека для визуализации данных.
-	Folium — библиотека для работы с картами и их визуализацией.
-	OpenWeather API — API для получения данных о погоде.

## Установка

### 1.	Клонируйте репозиторий:

```bash
git clone https://github.com/yourusername/weather-route-app.git
cd weather-route-app
```

### 2.	Создайте виртуальное окружение:

```bash
# На Windows:
python -m venv venv
.\venv\Scripts\activate

# На MacOS и Linux:
python3 -m venv venv
source venv/bin/activate
```

### 3.	Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```


### 4.	Получите API ключ от OpenWeather API:
-	Перейдите на OpenWeather и зарегистрируйтесь для получения API ключа.
-	После получения ключа, добавьте его в `.env` файл
```bash
echo OPEN_WEATHER_KEY = "YOUR_KEY" >> .env
```

### 5.	Запустите приложение:

```bash
python app.py
```

### 6. Открытие:
Откройте веб-браузер и перейдите по адресу http://127.0.0.1:8050/, чтобы начать использовать приложение.

## Использование
1.	Введите начальный город в поле “Введите начальный город”.
2.	Введите конечный город в поле “Введите конечный город”.
3.	Введите промежуточные города, если хотите, через запятую в поле “Введите промежуточные города”.
4.	Выберите город для отображения на графике с помощью выпадающего списка.
5.	Выберите параметры, которые хотите видеть на графике (температура, скорость ветра, осадки).
6.	Просматривайте прогноз погоды в виде графиков и на интерактивной карте.

## Зависимости

Приложение использует следующие библиотеки:
-	dash — для создания веб-приложений
-	plotly — для создания интерактивных графиков
-	folium — для отображения карт
-	requests — для работы с HTTP запросами
-	pandas — для обработки данных

Убедитесь, что установлены все зависимости, указанные в файле requirements.txt.

## Примечания
-	В случае, если приложение не может получить данные о погоде для города, будет показано сообщение о том, что данные недоступны.
-	Для работы с картой требуется стабильное интернет-соединение.