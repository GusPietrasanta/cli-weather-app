import geonamescache
import emoji
import flag
from geonamescache.mappers import country


# https://pypi.org/project/geonamescache/
gc = geonamescache.GeonamesCache(min_city_population=15000)
# 1 - Get city name from user
# 2 - Get city code from city
# 3 - Access to dictionary using city code
# 4 - Get both latitude and longitude like this:


countries_list = gc.get_countries_by_names()


def main():
    print(generate_ascii_art())

    city_data = get_user_input()
    city_name = city_data["name"]
    city_code = city_data["geonameid"]
    country_code = city_data["countrycode"]
    latitude = city_data["latitude"]
    longitude = city_data["longitude"]
    country = get_country_name_from_code(country_code)

    print("City name: ", city_name)
    print("City code: ", city_code)
    print("Country: ", country)
    print("Latitude: ", latitude)
    print("Longitude: ", longitude)


# Validate user input
def get_user_input():
    while True:
        user_input = input("What city would you like to know about the weather?: ")
        similar_results = gc.search_cities(user_input, case_sensitive=False, attribute="name")
        similar_results = sorted(similar_results, key=lambda d: d["population"], reverse=True)
        if len(similar_results) > 1:
            # If more than one city was found, show options:
            print("\nWell, we have a couple of coincidences here.")
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
                    user_selection = int(input(f"\nWhich one is the one you are after? (0 to {len(similar_results)}): "))
                except ValueError:
                    print("Not a valid option! Try again.")
                    continue
                if user_selection in option_lists:
                    city_data = similar_results[user_selection - 1]
                    return city_data
                else:
                    print("Not a valid option! Try again.")

        elif len(similar_results) == 0:
            # If no city was found, try again:
            print("\nSorry, no city found with that name.")
            print("Please try again.")
            continue
        else:
            city_name = similar_results[0]["name"]
            country_code = similar_results[0]["countrycode"]
            city_data = similar_results[0]
            country = get_country_name_from_code(country_code)
            print()
            while True:
                user_confirmation = input(f"Are we talking about {city_name}, {country} {flag.flag(country_code)}? (Y/N): ")
                if user_confirmation.lower() == "y" or user_confirmation.lower() == "yes":
                    return city_data
                elif user_confirmation.lower() == "n" or user_confirmation.lower() == "no":
                    print("\nOk, let's try again then.")
                    break
                else:
                    print("Not a valid option. Try again (Y/N): ")
                    continue


def generate_ascii_art():
    ...


def get_country_name_from_code(code):
    mapper = country(from_key="iso", to_key="name")
    return mapper(code)


# Call weather API and parse information
def function_n():
    ...


if __name__ == "__main__":
    main()
