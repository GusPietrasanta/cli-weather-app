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

- `generate_ascii_art()`: Creates a welcome message using `Figlet` module to generate a stylized "Weather CLI", surrounded by randomly chosen weather-related emojis.

- `get_user_input()`: Asks the user for a city and searches for similar cities names using `GeonamesCache` library, plus takes care of the error handling for user input. If no similar cities were found, prints an error message and prompts the user again for a city name. If more than one city was found, prints a list of options to the user to choose from. If only a city with that name was found, asks for confirmation. Finally, returns a dictionary containing information of the chosen city.

- `get_country_name_from_code(code)`: Uses the built-in mapper function from `GeonamesCache` to get the country full-name from a country code, since the city information dictionaries only contains country code and not the full name.
    - A bit more of information about the mapper module can be found in https://pypi.org/project/geonamescache/, "Mappers" section.

- `get_emoji_from_id(weather_id, timestamp, sunrise, sunset)`: Considering the passed `weather_id`, returns the appropriate weather emoji based on the weather conditions code that OpenWeather API uses. 
    - Weather condition codes list: https://openweathermap.org/weather-conditions
    - If the sky is clear, It will also return a sun emoji if the time in the city is between `sunrise` and `sunset` or a moon emoji if the time is between `sunset` and `sunrise`.

- `deg_to_compass(deg)`: Takes the wind direction degrees `deg` provided by the
    API response and "translates" it to more human-readable cardinal points
    - Implementation taken from: https://stackoverflow.com/questions/7490660/converting-wind-direction-in-angles-to-text-words
    - Credits to: https://stackoverflow.com/users/697151/steve-gregory

- `calculate_visibility(raw_visibility, units)`: Takes the `visibility` value returned by the API and simply divides it by 1000 if the value indicates "maximum visibility" (10000 metres) to use as default maximum visibility possible value, either 10.00 km or 10.00 miles. If the value is other than 10000, it converts it to miles if the chosen units system is Imperial. If the chosen units system is Metric, again simply returns the value divided by 1000 to use it as kilometres instead of metres.

- `generate_current_api_url(latitude, longitude, units)`: Generates the URL to access the current weather for the provided coordinates and with the chosen units.

- `ask_units()`: Asks what system of units the user would prefer to see the information and handles wrong user inputs while doing so.

- `set_units_current(units)`: Returns correct measurement units for temperature, speed and distance based on the previously chosen units to be used on the current weather.

- `set_units_forecast(units)`: Returns correct measurement units for temperature and speed based on the previously chosen units to be used on the weather forecast (Distance units not used when presenting 5 days forecast).

- `print_current_response(current_response, units)`: Takes the returned dictionary by `get_user_input()`, parses the relevant information, formats and prints the required data for the current weather.

- `ask_forecast()`: Asks the user if they would like to get a weather report for the next 5 days and handles bad user inputs while doing so.

- `print_forecast_response(forecast_response, units)`: Takes the returned dictionary by the second API call, parses the relevant information, formats and prints the required parameters for the 5 day / 3 hour weather forecast, looping through the returned list of dictionaries and converting the forecast time from UTC to local time.

- `generate_forecast_api_url(latitude, longitude, units)`: Generates the URL to access the 5 day weather forecast for the provided coordinates and with the previously chosen units.

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