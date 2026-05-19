from customtkinter import CTkImage
import customtkinter as ctk
from datetime import datetime
from time import strftime
import requests
from bs4 import BeautifulSoup
from tkinter import Label
from PIL import ImageTk, Image



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


#gui down


def update():
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

    ctk.set_appearance_mode("light")

    app = ctk.CTk()
    app.geometry("420x500")
    app.title("Weather App")

    #nighttime

    hour = datetime.now().hour
    #hour = 20

    if hour >= 20 or hour < 5:
        app.configure(fg_color="black")
        img = Image.open("moon.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="black", borderwidth=0, highlightthickness=0)
        label.pack(pady=(40, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="black")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="black")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkEntry(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=(current["temperature"]), font=("Arial", 50, "bold"),
                                  text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                 text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center",
                            text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center",
                                     text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

    #clear sky

    elif description == 0 or 1:
        app.configure(fg_color="sky blue")
        img = Image.open("Sun-Transparent-PNG.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="sky blue", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20,0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="sky blue")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="sky blue")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=str(current["temperature"]) + "°F", font=("Arial", 50, "bold"),
                                  text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center", text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"],"mph"), justify="center", text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center", text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

        #cloudy

    elif description == 2 or 3:
        app.configure(fg_color="gray")
        img = Image.open("clouds.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="gray", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="gray")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=str(current["temperature"]) + "°F", font=("Arial", 50, "bold"), text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                     text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center",
                                text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center",
                                    text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center",
                                         text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

    #Fog

    elif description == 45 or 48:
        app.configure(fg_color="gray")
        img = Image.open("Fog.jpg").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="gray", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="gray")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=str(current["temperature"]) + "°F", font=("Arial", 50, "bold"),
                                      text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18),
                                           text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                     text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center", text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center", text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

    #Rain
    elif description == 51 or 61 or 80:
        app.configure(fg_color="gray")
        img = Image.open("Rain.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="gray", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="gray")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=(current["temperature"]), font=("Arial", 50, "bold"),
                                  text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                 text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center",
                            text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center", text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

    #Snow
    elif description == 71:
        app.configure(fg_color="gray")
        img = Image.open("Rain.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="gray", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="gray")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=(current["temperature"]), font=("Arial", 50, "bold"),
                                  text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                 text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center",
                            text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center",
                                     text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)
    #Thunder

    elif description == 95:
        app.configure(fg_color="black")
        img = Image.open("Thunder.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="black", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="black")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="purple")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="black")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="purple")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=str(current["temperature"]) + "°F", font=("Arial", 50, "bold"),
                                  text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                 text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center",
                            text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center",
                                     text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

    #Rain

    elif description == 51 or 61 or 80:
        app.configure(fg_color="gray")
        img = Image.open("Rain.png").convert("RGBA")
        img = img.resize((230, 216))

        photo = ImageTk.PhotoImage(img)

        label = Label(app, image=photo, bg="gray", borderwidth=0, highlightthickness=0)
        label.pack(pady=(20, 0))

        main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"), text_color="yellow")
        title.pack(pady=(20, 10))

        search_frame = ctk.CTkFrame(main_frame, fg_color="gray")
        search_frame.pack(pady=10)

        city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
        city_entry.grid(row=0, column=0, padx=5)

        search_btn = ctk.CTkButton(search_frame, text="Search")
        search_btn.grid(row=0, column=1, padx=5)

        weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="blue")
        weather_card.pack(pady=20, padx=10, fill="both", expand=True)

        city_label = ctk.CTkLabel(weather_card, text=place, font=("Arial", 22), text_color="lightgray")
        city_label.pack(pady=(20, 5))

        temp_label = ctk.CTkLabel(weather_card, text=str(current["temperature"]) + "°F", font=("Arial", 50, "bold"),
                                  text_color="lightgray")
        temp_label.pack()

        condition_label = ctk.CTkLabel(weather_card, text=description, font=("Arial", 18), text_color="lightgray")
        condition_label.pack(pady=5)

        info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
        info_frame.pack(pady=20)

        feelslike = ctk.CTkLabel(info_frame, text=(f"Feels Like: {feels:.1f}°F"), justify="center",
                                 text_color="lightgray")
        feelslike.grid(row=2, column=0, padx=20)

        wind = ctk.CTkLabel(info_frame, text=("Windspeed:", current["windspeed"], "mph"), justify="center",
                            text_color="lightgray")
        wind.grid(row=0, column=1, padx=20)

        high = ctk.CTkLabel(info_frame, text=(f"High: {high_temp}°F"), justify="center", text_color="lightgray")
        high.grid(row=1, column=0, padx=20)

        low = ctk.CTkLabel(info_frame, text=(f"Low: {low_temp}°F"), justify="center", text_color="lightgray")
        low.grid(row=0, column=0, padx=20)

        humidity = ctk.CTkLabel(info_frame, text=(f"Humidity: {humidity}%"), justify="center", text_color="lightgray")
        humidity.grid(row=1, column=1, padx=20)

        precipitation = ctk.CTkLabel(info_frame, text=(f"Precipitation Chance: {precipitation}%"), justify="center",
                                     text_color="lightgray")
        precipitation.grid(row=2, column=1, padx=20)

    app.mainloop()
update()