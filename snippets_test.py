import geonamescache
from geonamescache.mappers import country

gc = geonamescache.GeonamesCache(min_city_population=15000)

countries_list = gc.get_countries_by_names()


def get_country_name_from_code(code):
    mapper = country(from_key="iso", to_key="name")
    return mapper(code)


user_input = input("What city would you like to know about the weather?: ")
similar_results = gc.search_cities(user_input, case_sensitive=False, attribute="name")
city_name = similar_results[0]["name"]
city_code = similar_results[0]["geonameid"]
country_code = similar_results[0]["countrycode"]
country = get_country_name_from_code(country_code)

sorted_results = sorted(similar_results, key=lambda d: d["population"], reverse=True)

print(similar_results)

print(sorted_results)
