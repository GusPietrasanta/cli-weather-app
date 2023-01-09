import argparse
import geonamescache


# https://pypi.org/project/geonamescache/
gc = geonamescache.GeonamesCache()
# 1 - Get city name from user
# 2 - Get city code from city
# 3 - Access to dictionary using city code
# 4 - Get both latitude and longitude like this:

# Get city:

similar_result = gc.search_cities("buenos aires", case_sensitive=False)

print(similar_result[0]["name"])

buenos_aires = gc.get_cities_by_name("Buenos Aires")

# Get code:
# print(buenos_aires[0].keys())
buenos_aires_code = list(buenos_aires[0].keys())
# print(list(buenos_aires_code)[0])

# Get latitude and longitude:
# print(buenos_aires[0]['3435910']['latitude'])
# print(buenos_aires[0]['3435910']['longitude'])
print(buenos_aires[0][buenos_aires_code[0]]["latitude"])
print(buenos_aires[0][buenos_aires_code[0]]["longitude"])


def main():
    ...


# Validate user input
# Use argparse library and complete usage text output
def function_1():
    ...


# Call Geocoding API and parse information
def function_2():
    ...


# Call weather API and parse information
def function_n():
    ...


if __name__ == "__main__":
    main()
