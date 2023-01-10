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

load_dotenv()

API_KEY = os.getenv("API_KEY")

# https://pypi.org/project/geonamescache/
gc = geonamescache.GeonamesCache(min_city_population=15000)

countries_list = gc.get_countries_by_names()


def main():
    print(generate_ascii_art())

    city_data = get_user_input()

    units = ask_units()

    temp_unit, speed_unit, distance_unit = set_units(units)

    city_name = city_data["name"]
    country_code = city_data["countrycode"]
    latitude = city_data["latitude"]
    longitude = city_data["longitude"]
    country = get_country_name_from_code(country_code)

    print(Fore.MAGENTA, end="")
    print("\nCity name:", city_name)
    print("Country:", country)
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print(Style.RESET_ALL, end="")

    # Here we go:
    api_url = generate_api_url(latitude, longitude, API_KEY, units)

    try:
        current_response = requests.get(api_url)
    except requests.RequestException:
        print(Fore.RED)
        sys.exit("Oops!Something went wrong." + Style.RESET_ALL)

    current_response = current_response.json()

    if current_response["cod"] != 200:
        print(Fore.RED)
        sys.exit("Oops!Something went wrong." + Style.RESET_ALL)

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
        weather_emoji = get_emoji_from_id(weather_id,
                                          timestamp,
                                          sunrise,
                                          sunset)
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
        timezone = current_response["timezone"]
        # Convert sunrise and sunset to local time
        sunrise = sunrise + timezone
        sunset = sunset + timezone
        sunrise = datetime.utcfromtimestamp(sunrise).strftime("%I:%M:%S %p")
        sunset = datetime.utcfromtimestamp(sunset).strftime("%I:%M:%S %p")
        last_updated = datetime.fromtimestamp(dt).strftime("%I:%M:%S %p")

        print(Fore.CYAN, end="")
        print(f"\nThe current weather in {city_name}, {country_name} is:\n")
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
        print(
            emoji.emojize(
                f":sunrise:  Sunrise: {sunrise} \
({city_name} time)"
            )
        )
        print(
            emoji.emojize(
                f":sunset:  Sunset: {sunset} \
({city_name} time)"
            )
        )
        print(
            emoji.emojize(
                f":hourglass_done:  Last updated: \
{last_updated} (Your time)\n"
            )
        )
        print(Style.RESET_ALL)


# Validate user input
def get_user_input():
    while True:
        user_input = input(
            Fore.GREEN
            + """What city would you like\
 to know about the weather?: """
            + Style.RESET_ALL
        )
        if len(user_input) < 3:
            print(
                emoji.emojize(
                    Fore.YELLOW
                    + """Sorry, that would return\
 a huge list :grinning_face_with_sweat:"""
                )
            )
            print(Fore.YELLOW + "Please be more specific." + Style.RESET_ALL)
            continue
        similar_results = gc.search_cities(
            user_input, case_sensitive=False, attribute="name"
        )
        similar_results = sorted(
            similar_results, key=lambda d: d["population"], reverse=True
        )
        if len(similar_results) > 1:
            # If more than one city was found, show options:
            print(Fore.YELLOW)
            print("Well, we have a couple of coincidences here.")
            print("(Sorted by population)\n")
            option_lists = []

            for i in range(len(similar_results)):
                option_lists.append(i + 1)
                city = similar_results[i]["name"]
                country_code = similar_results[i]["countrycode"]
                country = get_country_name_from_code(country_code)
                print(f"Option {i + 1}: {city}, {country}", end=" ")
                print(flag.flag(country_code))

            while True:
                try:
                    user_selection = int(
                        input(
                            Fore.YELLOW
                            + f"\nWhich one is the one you \
are after? (1 to {len(similar_results)}): "
                            + Style.RESET_ALL
                        )
                    )
                except ValueError:
                    print(Fore.RED)
                    print("Not a valid option! Try again.")
                    print(Style.RESET_ALL)
                    continue
                if user_selection in option_lists:
                    city_data = similar_results[user_selection - 1]
                    return city_data
                else:
                    print(Fore.RED)
                    print("Not a valid option! Try again.", end="")
                    print(Style.RESET_ALL)

        elif len(similar_results) == 0:
            # If no city was found, try again:
            print(Fore.RED)
            print("\nSorry, no city found with that name.")
            print("Please try again.\n")
            print(Style.RESET_ALL)
            continue
        else:
            city_name = similar_results[0]["name"]
            country_code = similar_results[0]["countrycode"]
            city_data = similar_results[0]
            country = get_country_name_from_code(country_code)
            while True:
                print(Fore.GREEN)
                user_confirmation = input(
                    f"Are we talking about {city_name},\
 {country} {flag.flag(country_code)}? (Y/N): " + Style.RESET_ALL
                )
                if (
                    user_confirmation.lower() == "y"
                    or user_confirmation.lower() == "yes"
                ):
                    return city_data
                elif (
                    user_confirmation.lower() == "n"
                    or user_confirmation.lower() == "no"
                ):
                    print(Fore.YELLOW)
                    print("Ok, let's try again then.")
                    print(Style.RESET_ALL)
                    break
                else:
                    print(Fore.RED)
                    print("Not a valid option. Try again (Y/N): ", end="")
                    print(Style.RESET_ALL)
                    continue


def generate_ascii_art():
    figlet = Figlet()

    font = "slant"

    figlet.setFont(font=font)

    text = "Weather CLI"

    emojis_list = [
        ":cloud:",
        ":cloud_with_lightning:",
        ":cloud_with_lightning_and_rain:",
        ":cloud_with_rain:",
        ":cloud_with_snow:",
        ":closed_umbrella:",
        ":sun_behind_cloud:",
        ":sun:",
        ":sun_behind_large_cloud:",
        ":sunrise:",
        ":sun_with_face:",
        ":sunrise_over_mountains:",
        ":sun_behind_small_cloud:",
        ":sun_behind_rain_cloud:",
        ":umbrella_with_rain_drops:",
        ":umbrella_on_ground:",
        ":umbrella:",
        ":snowflake:",
        ":snowman:",
        ":beach_with_umbrella:",
        ":desert_island:",
        ":water_wave:",
    ]

    emojis_to_print = 20
    string_to_return = ""

    string_to_return += "\n\n"
    for _ in range(emojis_to_print):
        string_to_return += emoji.emojize(random.choice(emojis_list)) + "  "
    string_to_return += "\n"
    string_to_return += Fore.CYAN + figlet.renderText(text)
    for _ in range(emojis_to_print - 2):
        string_to_return += emoji.emojize(random.choice(emojis_list)) + "  "
    string_to_return += "\n\n"

    return string_to_return


def get_country_name_from_code(code):
    mapper = country(from_key="iso", to_key="name")
    return mapper(code)


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


def ask_units():
    while True:
        user_preference = input(
            Fore.GREEN
            + """\nIn which units do you \
prefer the information? (M)etric or (I)mperial? """
            + Style.RESET_ALL
        ).lower()
        if user_preference == "m" or user_preference == "metric":
            return "metric"
        elif user_preference == "i" or user_preference == "imperial":
            return "imperial"
        else:
            print(Fore.RED)
            print("Sorry! Wrong input, please try again.", end="")
            print(Style.RESET_ALL)
            continue


def set_units(units):
    if units == "metric":
        return "°C", "meters/sec", "kms"
    elif units == "imperial":
        return "°F", "miles/hour", "miles"
    else:
        raise ValueError("Units were not properly defined.")


if __name__ == "__main__":
    main()
