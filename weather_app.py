from tkinter import *
import requests
from decouple import config
from datetime import datetime

api_key = config('API_KEY')

window = Tk()
window.geometry('500x500')
window.resizable(0, 0)
window.title('Simple weather app')

OPTIONS = ['Current Weather', '3-Day Forecast', '7-Day Forecast']

sbar = Scrollbar(window, orient='vertical')
sbar.pack(side=RIGHT, fill='y')

city = StringVar(window)
text_field = Text(window, width=45, height=17, yscrollcommand=sbar.set)
sbar.config(command=text_field.yview)

def reformat_date_time(dt_string, op='dt'):
    if op == 'dt':
        dt_obj = datetime.strptime(dt_string, '%Y-%m-%d %H:%M')
        return dt_obj.strftime('%A, %d/%m/%Y %H:%M')
    else:
        dt_obj = datetime.strptime(dt_string, '%Y-%m-%d')
        return dt_obj.strftime('%A, %d/%m/%Y')

def get_weather():
    city_name = city.get()
    weather_url = 'https://api.weatherapi.com/v1/'
    if option.get() == OPTIONS[0]:
        weather_url += f'current.json?key={api_key}&q={city_name}&aqi=no'
    else:
        weather_url += f'forecast.json?key={api_key}&q={city_name}&days={option.get()[0]}&aqi=no&alerts=no'
    response = requests.get(weather_url)
    weather_info = response.json()

    text_field.config(state=NORMAL)
    text_field.delete(1.0, END)

    if 'error' in weather_info.keys() or response.status_code != 200:
        print(f"Invalid URL: {weather_url}")
        print(f"Error message: {weather_info['error']['message']}")
        print(f"Status code: {response.status_code}")
        return
    
    if city_name == 'Enter city name...':
        output = 'Please enter a valid city, country or region name!'
        text_field.insert(INSERT, output)
        return
    
    output = f'{option.get()} for {city_name}\n\n'
    
    if option.get() == OPTIONS[0]:
        localtime = reformat_date_time(weather_info['location']['localtime'], 'dt')
        temp = int(weather_info['current']['temp_c'])
        condition = weather_info['current']['condition']['text']
        precip = weather_info['current']['precip_mm']
        wind = weather_info['current']['wind_kph']
        humidity = weather_info['current']['humidity']
        cloud = weather_info['current']['cloud']

        output += f'Local time: {localtime}\n\
Temperature: {temp}°C\n\
Condition: {condition}\n\
Cloud cover: {cloud}%\n\
Precipitation amount: {precip}mm\n\
Wind speed: {wind}km/h\n\
Humidity: {humidity}%'
        
    else:
        for forecastday in weather_info['forecast']['forecastday']:
            date = reformat_date_time(forecastday['date'], 'd')
            day = forecastday['day']
            maxtemp = day['maxtemp_c']
            mintemp = day['mintemp_c']
            precip = day['totalprecip_mm']
            condition = day['condition']['text']
            maxwind = day['maxwind_kph']
            avghumidity = day['avghumidity']
            rain_chance = day['daily_chance_of_rain']
            snow_chance = day['daily_chance_of_snow']
            output += f'Date: {date}\n\
Condition: {condition}\n\
Minimum temperature: {mintemp}°C\n\
Maximum temperature: {maxtemp}°C\n\
Chance of rain: {rain_chance}%\n\
Chance of snow: {snow_chance}%\n\
Total precipitation amount: {precip}mm\n\
Maximum wind speed: {maxwind}km/h\n\
Average humidity: {avghumidity}%\n\
\n'


    text_field.insert(INSERT, output)
    text_field.config(state=DISABLED)


def temp_text(e):
    city_entry.delete(0, END)

city_entry = Entry(window, textvariable=city, width=24)
city_entry.insert(0, 'Enter city name...')
city_entry.pack(pady=20)
city_entry.bind('<FocusIn>', temp_text)

option = StringVar(window)
option.set(OPTIONS[0])

options_menu = OptionMenu(window, option, *OPTIONS)
options_menu.pack()


Button(window, command=get_weather, text='Check Weather', 
       bg='lightblue', fg='black', activebackground='teal', 
       padx=5, pady=5).pack(pady=20)

text_field.pack()

window.mainloop()