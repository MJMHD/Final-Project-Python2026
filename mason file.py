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
        "hourly": "relative_humidity_2m,precipitation_probability",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    data = response.json()

    current = data["current_weather"]
    humidity = data["hourly"]["relative_humidity_2m"][0]
    precipitation = data["hourly"]["precipitation_probability"][0]
    temp = current["temperature"]
    wind = current["windspeed"]
    high_temp = data["daily"]["temperature_2m_max"][0]
    low_temp = data["daily"]["temperature_2m_min"][0]

    feels = feels_like(temp, wind)

    return current, humidity, precipitation, feels,  high_temp, low_temp

def feels_like(temp, wind):
    # simple approximation (not perfect, but good for projects)

    if temp <= 50:  # cold weather (wind chill style)
        return temp - (wind * 0.7)
    else:  # warmer weather
        return temp + (wind * 0.1)


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


def feels_like(temp, wind):
    # simple approximation (not perfect, but good for projects)

    if temp <= 50:  # cold weather (wind chill style)
        return temp - (wind * 0.7)
    else:  # warmer weather
        return temp + (wind * 0.1)

lat, lon = get_lat_lon(place)

if lat and lon:
    current, humidity, precipitation, feels, high_temp, low_temp = get_weather(lat, lon)


    description = get_weather_description(current["weathercode"])

    print(f"Temperature: {current['temperature']}°F")
    print(f"Wind Speed: {current['windspeed']} mph")
    print(f"Humidity: {humidity}%")
    print(f"Condition: {description}")
    print(f"Precipitation Chance: {precipitation}%")
    print(f"Feels Like: {feels:.1f}°F")
    print(f"High: {high_temp}°F")
    print(f"Low: {low_temp}°F")
else:
    print("Location not found")


































































































