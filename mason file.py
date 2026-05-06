import customtkinter
from datetime import datetime
from time import strftime
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from customtkinter import CTkImage
import requests



def get_lat_lon(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": place, "format": "json"}
    headers = {"User-Agent": "my-app"}

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    return None, None



def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True,
        "hourly": "relative_humidity_2m"
    }

    response = requests.get(url, params=params)
    data = response.json()

    current = data["current_weather"]
    humidity = data["hourly"]["relative_humidity_2m"][0]

    return current, humidity
def get_weather_description(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Freezing fog",
        51: "Light drizzle",
        61: "Rain",
        71: "Snow",
        80: "Rain showers",
        95: "Thunderstorm"
    }
    return weather_codes.get(code, "Unknown")
place = input("Enter a location: ")

lat, lon = get_lat_lon(place)

if lat and lon:
    current, humidity = get_weather(lat, lon)

    description = get_weather_description(current["weathercode"])

    print(f"Temperature: {current['temperature']}°C")
    print(f"Wind Speed: {current['windspeed']} km/h")
    print(f"Humidity: {humidity}%")
    print(f"Condition: {description}")
else:
    print("Location not found")


































































































