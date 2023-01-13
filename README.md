# Weather CLI

#### Video Demo: <URL HERE>

#### Description:

Weather CLI was coded as my final project for Harvard's CS50’s Introduction to Programming with Python. It's a command line interface weather app that asks the user for the city is willing to know the weather about, uses the [GeonamesCache library](https://pypi.org/project/geonamescache/) to get the geographic coordinates (latitude and longitude), also asks for the required units to present the information (metric or imperial) and gets the current weather using the [OpenWeather API](https://openweathermap.org/api). Finally asks the user if they would like to obtain a 5 day / 3 hour forecast for the same city, calls the API to the new required information and presents it to the screen organized by days if the user accepted so.

### Imports:

- Imports `os` to read environment variables where the API key will be stored.
- Imports `sys` to exit the program when something goes wrong.
- Imports `flag` to print to the terminal country flags (sadly only prints the country code and not the flag, but I hope one day the country flags will be added as emojis and this little feature will be finally fully supported and useful :) )
- Imports `emoji` to print weather-related emojis while presenting the information and it's also used with some ASCII Art as welcome message.
- Imports `random` to choose some random emojis from a list while generating the welcome message.
- Imports `requests` to handle API calls.
- Imports `geonamescache` to get a list of cities and their coordinates.
- Imports `pyfiglet` to print a stylized "Weather CLI" welcome message.
- Imports `datetime` to handle the timestamps returned by the API, sunrise and sunset times, convert returned UTC to local or user time, etc.
- Imports `dotenv` to read the API key from the .env file.
- Imports `colorama` to print colored output on Windows terminal, presenting error messages in red, normal program questions in green, "conflicts" in yellow, city information in magenta, and weather information in cyan.

## Initial Setup 

- Complete "API_KEY = ..." on line 18 with your own API key from [OpenWeather API](https://openweathermap.org/)

- For a more complete list of available cities replace default value of min_city_population=15000 with 500, 1000 or 5000.

## How Weather CLI Works:

- `main()`:
    1. Prints welcome message calling `generate_ascii_art()`.
    2. Calls `get_user_input()` to get the city name.
    3. Prompts the user for the desired units to use calling `ask_units()`.
    4. Parses some information from the required city, generates a couple of variables and prints the information to the terminal.
    5. Calls `generate_current_api_url()` to generate the URL to be used to make the API call, passing the previously gathered coordinates and measurement units.
    6. Executes the API call, parses the response and stores the returned respone as `current_response()`.
    7. If the returned status response code IS NOT HTTP 200 OK success, exit the program.
    8. Calls `print_current_response()` passing the just returned response and the selected measurement units.
    9. Asks user if they want to get a 5 day forecast for the same city calling `ask_forecast()` and storing the response as a boolean.
    10. If the user responded yes, `wants_forecast` will be true, and a new API URL will be generated using the same coordinates a units but this time using `generate_forecast_api_url()` to contact the right end point.
    11. Calls the API with the generated URL.
    12. Stores the response as `forecast_response`.
    13. Again, if the returned status response code IS NOT HTTP 200 OK success, exit the program.
    14.  Calls `print_forecast_response()` passing the new returned response and the selected measurement units.
    15. Prints goodbye message.

## Functions

- `get_user_input()`: TODO

- `generate_ascii_art()`: TODO

- `get_country_name_from_code(code)`: TODO

- `get_emoji_from_id(weather_id, timestamp, sunrise, sunset)`: TODO

- `deg_to_compass(deg)`: TODO

- `calculate_visibility(raw_visibility, units)`: TODO

- `generate_current_api_url(latitude, longitude, units)`: TODO

- `ask_units()`: TODO

- `set_units_current(units)`: TODO

- `set_units_forecast(units)`: TODO

- `print_current_response(current_response, units)`: TODO

- `ask_forecast()`: TODO

- `print_forecast_response(forecast_response, units)`: TODO

- `generate_forecast_api_url(latitude, longitude, units)`: TODO

## Use Examples:
TODO

#### Welcome Message
TODO

#### Multiple Cities Found (min_city_population=15000)
TODO

#### Multiple Cities Found (min_city_population=500)
TODO

#### No City Found
TODO

#### Only One City Found
TODO

#### Wrong User Selection
TODO

#### Asking for Units
TODO

#### Printing Information Using Metric System
TODO

#### Printing Information Using Imperial System
TODO

#### User Being Asked If They'd Like A 5 Day Forecast
TODO

#### Printing Information Using Metric System
TODO

#### Printing Information Using Imperial System
TODO

#### Note the sun or moon emoji wether forecast time is between sunrise and sunset.
TODO