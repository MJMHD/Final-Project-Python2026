import customtkinter as ctk
from datetime import datetime
from time import strftime
import requests
from bs4 import BeautifulSoup
from tkinter import Label
from PIL import ImageTk, Image

def update():
    ctk.set_appearance_mode("light")

    app = ctk.CTk()
    app.geometry("420x500")
    app.title("Weather App")
    app.configure(fg_color="sky blue")

    img = Image.open("Sun-Transparent-PNG.png").convert("RGBA")
    img = img.resize((230, 216))

    photo = ImageTk.PhotoImage(img)

    label = Label(app, image=photo, bg="sky blue", borderwidth=0, highlightthickness=0)
    label.pack(pady=(40,0))

    #img = Image.open("clouds.png").convert("RGBA")
    #img = img.resize((230, 216))

    #photo = ImageTk.PhotoImage(img)

    #label = Label(app, image=photo, bg="gray", borderwidth=0, highlightthickness=0)
    #label.pack(pady=(40, 0))

    #img = Image.open("moon.png").convert("RGBA")
    #img = img.resize((230, 216))

    #photo = ImageTk.PhotoImage(img)

    #label = Label(app, image=photo, bg="black", borderwidth=0, highlightthickness=0)
    #label.pack(pady=(40, 0))

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

    city_label = ctk.CTkLabel(weather_card, text="New York", font=("Arial", 22), text_color="lightgray")
    city_label.pack(pady=(20, 5))

    temp_label = ctk.CTkLabel(weather_card, text="22°C", font=("Arial", 50, "bold"), text_color="lightgray")
    temp_label.pack()

    condition_label = ctk.CTkLabel(weather_card, text="Sunny ☀️", font=("Arial", 18), text_color="lightgray")
    condition_label.pack(pady=5)

    info_frame = ctk.CTkFrame(weather_card, fg_color="transparent")
    info_frame.pack(pady=20)

    humidity = ctk.CTkLabel(info_frame, text="Humidity\n60%", justify="center", text_color="lightgray")
    humidity.grid(row=0, column=0, padx=20)

    wind = ctk.CTkLabel(info_frame, text="Wind\n12 km/h", justify="center", text_color="lightgray")
    wind.grid(row=0, column=1, padx=20)

    app.mainloop()
update()