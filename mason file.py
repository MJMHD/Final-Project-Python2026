import customtkinter
from datetime import datetime
from time import strftime
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image
from customtkinter import CTkImage

root = customtkinter.CTk()

root.geometry("375x400")

import requests

def get_lat_lon(place):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": place,
        "format": "json"
    }
    headers = {
        "User-Agent": "my-geocoder-app"  # required
    }

    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:  # make sure we got results
        lat = data[0]["lat"]
        lon = data[0]["lon"]
        return lat, lon
    else:
        return None, None


# Example usage
place = input("Enter a location: ")
lat, lon = get_lat_lon(place)

if lat and lon:
    print(f"Latitude: {lat}, Longitude: {lon}")
else:
    print("Location not found.")




print(get_lat_lon("Charlotte, North Carolina"))
def update_code():
    localcurrentdateandtime = datetime.now()
    currentdatetime = localcurrentdateandtime.strftime("%m/%d/%Y")

    url = "https://forecast.weather.gov/MapClick.php?lat=", + "LA", + "&lon=""", + "LO"

























































































