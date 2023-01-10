import os
import sys
import emoji
import requests
from dotenv import load_dotenv
from datetime import datetime
from project import get_country_name_from_code

load_dotenv()

latitude = "-34.92866"

longitude = "138.59863"

API_KEY = os.getenv("API_KEY")

units = "metric"


# Weather now
def main():

    if units == "metric":
        temp_unit = "°C"
        speed_unit = "meters/sec"
        distance_unit = "kms"
    elif units == "imperial":
        temp_unit = "°F"
        speed_unit = "miles/hour"
        distance_unit = "miles"
    else:
        raise ValueError("Units were not properly defined.")

    api_url = generate_api_url(latitude, longitude, API_KEY, units)

    try:
        current_response = requests.get(api_url)
    except requests.RequestException:
        sys.exit("Oops!Something went wrong.")

    current_response = current_response.json()

    if current_response["cod"] != 200:
        sys.exit("Oops!Something went wrong.")

    else:
        timestamp = current_response["dt"]
        city_name = current_response["name"]
        country_code = current_response["sys"]["country"]
        country_name = get_country_name_from_code(country_code)

        weather_id = str(current_response["weather"][0]["id"])
        main = current_response["weather"][0]["main"]
        description = current_response["weather"][0]["description"]
        sunrise = current_response["sys"]["sunrise"]
        sunset = current_response["sys"]["sunset"]
        weather_emoji = get_emoji_from_id(weather_id, timestamp, sunrise, sunset)
        temp = current_response["main"]["temp"]
        feels_like = current_response["main"]["feels_like"]
        temp_min = current_response["main"]["temp_min"]
        temp_max = current_response["main"]["temp_max"]
        pressure = current_response["main"]["pressure"]
        humidity = current_response["main"]["humidity"]
        raw_visibility = current_response["visibility"]
        visibility = calculate_visibility(raw_visibility, units)
        wind_speed = current_response["wind"]["speed"]
        wind_direction = deg_to_compass(current_response["wind"]["deg"])
        clouds = current_response["clouds"]["all"]
        dt = current_response["dt"]
        sunrise_print = datetime.fromtimestamp(sunrise).strftime("%I:%M:%S %p")
        sunset_print = datetime.fromtimestamp(sunset).strftime("%I:%M:%S %p")
        last_updated = datetime.fromtimestamp(dt).strftime("%I:%M:%S %p")

        print(f"The current weather in {city_name}, {country_name} is:")
        print(emoji.emojize(f"{weather_emoji}   {main} ({description})"))
        print(emoji.emojize(f":thermometer:   Temperature: {temp}{temp_unit}"))
        print(
            emoji.emojize(
                f""":person_mountain_biking:\
  Feels Like: {feels_like}{temp_unit}"""
            )
        )
        print(
            emoji.emojize(
                f""":red_circle:  Max currently\
 observed temperature in {city_name}: {temp_max}{temp_unit}"""
            )
        )
        print(
            emoji.emojize(
                f""":blue_circle:  Min currenty observed\
 temperature in {city_name}: {temp_min}{temp_unit}"""
            )
        )
        print(emoji.emojize(f":balance_scale:   Pressure: {pressure} hPa"))
        print(emoji.emojize(f":droplet:  Humidity: {humidity}%"))
        print(
            emoji.emojize(
                f""":telescope:  Visibility:\
 {visibility:.2f} {distance_unit}"""
            )
        )
        print(
            emoji.emojize(
                f""":wind_face:   Wind speed:\
 {wind_speed} {speed_unit}"""
            )
        )
        print(emoji.emojize(f":compass:  Wind direction: {wind_direction}"))
        print(emoji.emojize(f":cloud:   Cloudiness: {clouds}%"))
        print(emoji.emojize(f":sunrise:  Sunrise: {sunrise_print}"))
        print(emoji.emojize(f":sunset:  Sunset: {sunset_print}"))
        print(emoji.emojize(f":hourglass_done:  Last updated: {last_updated}"))


def get_emoji_from_id(id, timestamp, sunrise, sunset):
    if id.startswith("2"):
        return ":cloud_with_lightning_and_rain:"
    elif id.startswith("3"):
        return ":cloud_with_rain:"
    elif id.startswith("5"):
        return ":cloud_with_rain:"
    elif id.startswith("6"):
        return ":snowflake:"
    elif id.startswith("7"):
        return ":fog:"
    elif id == "800":
        if timestamp > sunrise and timestamp < sunset:
            return ":sun:"
        else:
            return ":last_quarter_moon:"
    elif id.startswith("8"):
        return ":cloud:"
    else:
        return ""


def deg_to_compass(deg):
    """
    Implementation taken from:
    https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
    Credits to: https://stackoverflow.com/users/697151/steve-gregory
    """
    value = int((deg / 22.5) + 0.5)
    compass_directions = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
    ]
    return compass_directions[(value % 16)]


def calculate_visibility(raw_visibility, units):
    if raw_visibility == 10000:
        visibility = raw_visibility / 1000.00
    else:
        if units == "imperial":
            visibility = (raw_visibility / 1000) / 1.609
        else:
            visibility = raw_visibility / 1000.00
    return round(visibility, 2)


def generate_api_url(latitude, longitude, API_KEY, units):
    return f"""https://api.openweathermap.org/data/2.5/weather?\
lat={latitude}&lon={longitude}&appid={API_KEY}&units={units}"""


if __name__ == "__main__":
    main()
