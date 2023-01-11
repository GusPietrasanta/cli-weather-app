import os
import sys
import flag
import emoji
import random
import requests
import geonamescache
from pyfiglet import Figlet
from datetime import datetime
from dotenv import load_dotenv
from geonamescache.mappers import country
from colorama import Fore, Back, Style
from forecast_response import forecast_response
from datetime import datetime
import emoji
from colorama import Fore, Back, Style
from project import (get_country_name_from_code,
                     get_emoji_from_id,
                     calculate_visibility,
                     deg_to_compass,
                     set_units)

# print(response["list"][0])
load_dotenv()
API_KEY = os.getenv("API_KEY")
latitude = -34.92866
longitude = 138.59863
units = "metric"


def generate_forecast_api_url(latitude, longitude, units):
    return f"""https://api.openweathermap.org/data/2.5/forecast?\
lat={latitude}&lon={longitude}&appid={API_KEY}&units={units}"""


# Here we go:
forecast_api_url = generate_forecast_api_url(latitude, longitude, units)

print(forecast_api_url)

try:
    forecast_response = requests.get(forecast_api_url)
except requests.RequestException:
    print(Fore.RED)
    sys.exit("Oops!Something went wrong." + Style.RESET_ALL)

forecast_response = forecast_response.json()

if forecast_response["cod"] != "200":
    print(Fore.RED)
    sys.exit("Oops!Something went wrong." + Style.RESET_ALL)
else:
    temp_unit, speed_unit, distance_unit = set_units(units)

    city_name = forecast_response["city"]["name"]
    sunrise = forecast_response["city"]["sunrise"]
    sunrise = datetime.fromtimestamp(sunrise)
    sunset = forecast_response["city"]["sunset"]
    sunset = datetime.fromtimestamp(sunset)
    timezone = int(forecast_response["city"]["timezone"])
    # Convert sunrise and sunset to local time
    date = ""
    print()

    for forecast in forecast_response["list"]:
        timestamp = forecast["dt"]

        local_time = timestamp
        new_date = datetime.fromtimestamp(local_time).strftime("%A, %d %B %Y")

        timestamp = datetime.fromtimestamp(timestamp)

        weather_id = str(forecast["weather"][0]["id"])
        main = forecast["weather"][0]["main"]
        description = forecast["weather"][0]["description"]
        weather_emoji = get_emoji_from_id(weather_id,
                                          timestamp.hour,
                                          sunrise.hour,
                                          sunset.hour)
        temp = forecast["main"]["temp"]
        pressure = forecast["main"]["pressure"]
        humidity = forecast["main"]["humidity"]
        wind_speed = forecast["wind"]["speed"]
        wind_direction = deg_to_compass(forecast["wind"]["deg"])
        clouds = forecast["clouds"]["all"]
        dt = forecast["dt"]

        forecast_time = datetime.fromtimestamp(dt).strftime("%I:%M:%S %p")

        print(Fore.YELLOW, end="")
        if new_date != date:
            print(emoji.emojize(f":calendar:  {new_date}"))
            date = new_date
        print(Fore.MAGENTA, end="")
        print(emoji.emojize(f":hourglass_done:  {forecast_time} \
    ({city_name} time)"))
        print(Fore.CYAN, end="")
        print(emoji.emojize(f"{weather_emoji}   {main} ({description})  \
    :thermometer:  Temperature: {temp}{temp_unit}  :balance_scale:   \
Pressure: {pressure} hPa"))
        print(emoji.emojize(f":droplet:  Humidity: {humidity}%      \
    :wind_face:   Wind: {wind_speed} {speed_unit} {wind_direction}   :cloud:  \
Cloudiness: {clouds}%"))
        print(Style.RESET_ALL)
