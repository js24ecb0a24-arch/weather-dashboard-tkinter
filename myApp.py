
from tkinter import *
import tkinter.font as font
import requests
from PIL import Image, ImageTk
from datetime import datetime

# Constants
API_KEY = "YOUR_API_KEY"

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast?"

WEATHER_ICONS = {
    "Clear": "icons/clear.png",
    "Clouds": "icons/cloudy.png",
    "Rain": "icons/rain.png",
    "Snow": "icons/snow.png",
    "Drizzle": "icons/drizzle.png",
    "Thunderstorm": "icons/thunderstorm.png",
}

root = Tk()
root.title("Weather Conditions")

myfont = font.Font(family='Helvetica', size=20, weight='bold')
myfontbig = font.Font(family='Helvetica', size=60, weight='bold')
myfontsmall = font.Font(family='Helvetica', size=15)

frame = LabelFrame(root)
frame.pack(padx=10, pady=10)

def get_weather_icon(weather):
    return WEATHER_ICONS.get(weather, "icons/clear.png")

def submit():
    city = entry.get()
    entry.delete(0, END)

    complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city
    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":

        cityog = x['name']
        country = x['sys']['country']

        current_temp = round(x['main']['temp'] - 273.15, 1)
        feels_like = round(x['main']['feels_like'] - 273.15, 1)

        weather = x['weather'][0]['main']

        min_temp = round(x['main']['temp_min'] - 273.15, 1)
        max_temp = round(x['main']['temp_max'] - 273.15, 1)

        top = Toplevel()

        frame2 = LabelFrame(top)
        frame2.pack(padx=10, pady=10)

        label1 = Label(frame2, text=f"{cityog}, {country}")
        label1['font'] = myfont
        label1.grid(column=1, row=0)

        label2 = Label(frame2, text=f"{current_temp} °C")
        label2['font'] = myfontbig
        label2.grid(column=1, row=1)

        weather_icon_path = get_weather_icon(weather)

        weather_icon = Image.open(weather_icon_path)
        weather_icon = weather_icon.resize((100, 100), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(weather_icon)

        icon_label = Label(frame2, image=weather_icon)
        icon_label.image = weather_icon
        icon_label.grid(column=1, row=2)

        frame3 = LabelFrame(frame2)
        frame3.grid(column=1, row=3, pady=5)

        label3 = Label(frame3, text=f"Feels like {feels_like} °C", anchor=W)
        label3['font'] = myfontsmall
        label3.grid(column=1, row=3, columnspan=2)

        label4 = Label(frame3, text=weather)
        label4['font'] = myfont
        label4.grid(column=1, row=2)

        label5 = Label(
            frame3,
            text=f"Min/Max temp: {min_temp}°/{max_temp}°"
        )
        label5['font'] = myfontsmall
        label5.grid(column=1, row=4)

        get_forecast(city)

def get_forecast(city):

    complete_url = FORECAST_URL + "appid=" + API_KEY + "&q=" + city

    response = requests.get(complete_url)

    forecast_data = response.json()

    if forecast_data["cod"] != "404":

        forecast_window = Toplevel()
        forecast_window.title(f"5-Day Forecast for {city}")

        forecast_frame = LabelFrame(
            forecast_window,
            text="5-Day Forecast",
            padx=10,
            pady=10
        )

        forecast_frame.pack(padx=10, pady=10)

        for i, day in enumerate(forecast_data['list']):

            if i % 8 == 0:

                date = datetime.fromtimestamp(
                    day['dt']
                ).strftime('%Y-%m-%d')

                temp = round(day['main']['temp'] - 273.15, 1)

                description = day['weather'][0]['main']

                weather_icon_path = get_weather_icon(description)

                weather_icon = Image.open(weather_icon_path)
                weather_icon = weather_icon.resize((50, 50), Image.LANCZOS)
                weather_icon = ImageTk.PhotoImage(weather_icon)

                day_label = Label(
                    forecast_frame,
                    text=f"{date}: {temp}°C, {description}"
                )

                day_label.grid(
                    row=i // 8,
                    column=0,
                    padx=5,
                    pady=5
                )

                icon_label = Label(
                    forecast_frame,
                    image=weather_icon
                )

                icon_label.image = weather_icon

                icon_label.grid(
                    row=i // 8,
                    column=1,
                    padx=5,
                    pady=5
                )

Label(
    frame,
    text="Enter City Name:",
    font=myfont
).grid(column=1, row=0)

entry = Entry(frame)

entry['font'] = myfont

entry.grid(
    column=0,
    row=1,
    columnspan=3,
    padx=10,
    pady=10,
    ipadx=50,
    ipady=5
)

button = Button(
    frame,
    text="Submit",
    command=submit
)

button['font'] = myfont

button.grid(
    column=1,
    row=2,
    ipadx=20,
    pady=10
)

root.mainloop()
