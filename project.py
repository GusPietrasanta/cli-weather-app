import argparse
import geonamescache


# https://pypi.org/project/geonamescache/
gc = geonamescache.GeonamesCache()
buenos_aires = gc.get_cities_by_name("Buenos Aires")
print(buenos_aires[0]['3435910']['latitude'])
print(buenos_aires[0]['3435910']['longitude'])


def main():
    ...


# Validate user input
# Use argparse library and complete usage text output
def function_1():
    ...


# Read csv?
# List of countries first maybe?
# List of cities first maybe?


# Call Geocoding API and parse information
def function_2():
    ...


# Call weather API and parse information
def function_n():
    ...


if __name__ == "__main__":
    main()
