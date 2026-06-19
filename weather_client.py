from dotenv import load_dotenv
from exceptions import CityNotFoundError
from exceptions import WeatherProviderError
import requests
import os

load_dotenv()
key = os.environ.get("OPENWEATHER_API_KEY")

def _handle_weather_response(response, city):
    """Check status_code and either return parsed JSON or raise the right exception."""
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise CityNotFoundError(f"City '{city}' not found.")
    else:
        raise WeatherProviderError(f"OpenWeatherMap returned status {response.status_code}")

def get_current_weather(city):
    """fetch the current weather of the city"""
    weather = requests.get("https://api.openweathermap.org/data/2.5/weather", params={"q": city, "appid": key, "units": "metric"})
    return _handle_weather_response(weather, city)

def get_forecast(city):
    """fetch the 5-day/3-hour forecast for the city"""
    response = requests.get("https://api.openweathermap.org/data/2.5/forecast", params={"q": city, "appid": key, "units": "metric"})
    return _handle_weather_response(response, city)
