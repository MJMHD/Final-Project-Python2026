import customtkinter as ctk
from datetime import datetime
from time import strftime
import requests
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

def update():
    localcurrentdateandtime = datetime.now()
    currentdatetime = localcurrentdateandtime.strftime("%m/%d/%Y")

    url = "https://www.weather.gov/"

    html = requests.get(url).content

    soup = BeautifulSoup(html, 'html.parser')

    ctk.set_appearance_mode("light")

    app = ctk.CTk()
    app.geometry("420x500")
    app.title("Weather App")
    app.configure(fg_color="sky blue")

    main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="sky blue")
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    title = ctk.CTkLabel(main_frame, text="Weather", font=("Arial", 28, "bold"))
    title.pack(pady=(20, 10))

    search_frame = ctk.CTkFrame(main_frame, fg_color="sky blue")
    search_frame.pack(pady=10)

    city_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter city...", width=200)
    city_entry.grid(row=0, column=0, padx=5)

    search_btn = ctk.CTkButton(search_frame, text="Search")
    search_btn.grid(row=0, column=1, padx=5)

    weather_card = ctk.CTkFrame(main_frame, corner_radius=20, fg_color="sky blue")
    weather_card.pack(pady=20, padx=10, fill="both", expand=True)

    city_label = ctk.CTkLabel(weather_card, text="New York", font=("Arial", 22))
    city_label.pack(pady=(20, 5))

    temp_label = ctk.CTkLabel(weather_card, text="22°C", font=("Arial", 50, "bold"))
    temp_label.pack()

    condition_label = ctk.CTkLabel(weather_card, text="Sunny ☀️", font=("Arial", 18))
    condition_label.pack(pady=5)

    info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
    info_frame.pack(pady=20)

    humidity = ctk.CTkLabel(info_frame, text="Humidity\n60%", justify="center")
    humidity.grid(row=0, column=0, padx=20)

    wind = ctk.CTkLabel(info_frame, text="Wind\n12 km/h", justify="center")
    wind.grid(row=0, column=1, padx=20)

    app.mainloop()
update()