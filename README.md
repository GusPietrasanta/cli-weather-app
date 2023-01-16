# Weather CLI

#### Video Demo: https://www.youtube.com/watch?v=nd-VpkDMXHU

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
- Imports `pyfiglet` to generate a stylized "Weather CLI" welcome message.
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

#### Welcome Message
![](https://lh3.googleusercontent.com/pgkVBhjaAGBwpPJR1nG2XjmpPMzwp1W-ya69dXXeMofebCc6CdnwqVqjMRxHJcpLwkpv4EeNowse0xQQP55PuPx8Yk15XvoQappSUZXypSscioIrE1tSqYPmX3hqpJKoiWRqe_TreUHAO2UIfR5H1CSoBgws5O0uvbkZt4QIODsbOKWET08mApT3jVRn93uvJLKVPYL8m-jvZWlb-Qi4K8DfDs0frgH7Q2rsbcD4WL6osL10HUoZ-XxbF-3hXJ7ioncAdGKXI6pL6EJBIaDTD7e-vjcYYutTppnvZswhCP0-QZyvvsAoc6Lv-mL4kVuXXBHtuIAnLWZ2iYr2BnCnF6YWGcSRiETuVEv-xK4apsoGVJdeT4hFfmfx3LxhWH5FYQTuIvG1t_ymVOtwyvAcZVhDcZZcTd2SSVru9LcsK80V4WoOiIWYLH_J1-KiphqvXk6nJxEtJAUoF5mGd4L4h3G5AVWWdrSNMk2_l7v1OCCTOWS4K5chF2bojTEtHZaAmPJ9PjSka4AsbYyDD5OG27uIMDPkgh_D959FhAiqEeq70X1sk2pEDCljAsDvvKgeS9Cb9nsQRvEBPQ_dWWJIam5VB_0CRdKySTnqMo7v9QJsXE49O58aqPyUYH9eSmKva0-Mf0xqHz_NOE18a9sSMRtAsW7OPI3cb5sMiMDMNuzvLDq_om_Annvvikv2PHcvIlhsrrPpV-WyfeNRejBt_vwUOjH-pO2-_hX2ZRQ9u-btnZ1y3Ita_ahABf9nZ0gqS5FcJtSuWBSOXec0lb-1ppXP9DUmvHilQ9VjCNEIQ_kPFKJqx18YDz-P5tEDRlE_pENkoP2taWIThfjUYNUUuYjsMux4nefriGVKp1r6sk1bessvKTMsq2KGWPftCLXiZ0LLxY4RvZJsFxzs1pE4g9SQzWy-W6ditwAyziVp1VEX=w626-h268)

#### Multiple Cities Found (min_city_population=15000)
![](https://lh3.googleusercontent.com/3X53icQ9a28HEby6gheb5J3nlnhYrrZbLVfJx0cnkwirrsvuocZedWNJ5qpqQoffGlLQkq4eRb1FGbbZG-utMasGGaBE-eLKOGkkiGJQpli2uLV0aQ54wDE57xGNhe-7hIO7AKkjHfU2SgZVjh7DiexWTTjEQB6jvJZmtz16Sss0UKLE6dBWtSCM8K0DiHKf7-aQ9xYwwDV4-TUsuQBjWtLC9WgCiz1Ovz5QmcGk5LbZY67Ochh8H2xyZhAK_UzpNvx6Guihk9SIXwePOxgMSh4v1teQ9SHIJAIPIFLS7WKiH0b7tdrxyYGI431XpxK0v0aKnzJHFqtfrqZuynYcSiZa1rGvYNXE0wZ6-QgNslU3h7jZc38c5X0pXZ_Hp_9zv5cPTNIw-ic9je3G686Iq64DInHj8pcEIHmd4tTOzeOjXzO6_44fL__nU2XHufpx45vCu8_PRoJtarhgDFe3TSp2umQnF__0QFhaTMqODg2LPwmGJlkHc4P-_kRuA1i5Wi0mdxow0Y5pO5Ow8LaTd2pwxd4FqQ78WeimmYy3-pAN-2PkynwiFF4UWSgllQqZIkVbBr7YE-i1c2Y_kJqiXuBL1lVD4ML9uXRPsiSR1vd--SGQqvBBp7oZrdNRm80CBux8Emia4iwQAQMfKdI0OU44BR4dTTkLtRdO5W8WtfwlURZl0K9ecvMJDHWKls4ItdVlUwvLLiC1ZhH7wVKFIJ-a9utfkE7EtkjKqQbzofjFTTJwluz7fWHpyGLkvmn7RYSqqSP6wpA8jxt8HxDvQwrdnbgPDGDk_21LLuXAFiH5A1P9RPh6j1Fz33AwyQEH1Hc8dxl0wx75jdtXxumeZZCS2lj7VHSJmdjh02mUURnKI_eF9GQK3CFY2ngxSGyPpfXxcdlIVDJteCkhRoObkqn3fOEfCqxaaQM5SFSqIceg=w628-h451)

#### Multiple Cities Found (min_city_population=500)
![](https://lh3.googleusercontent.com/EKlZIvYArGarp2gfkDTsqWi5DDTnRDiVh3S6RBhkjJy7o0N4tpvAdiksvz9L88WHqmMEkLReYtpVyAuyfVdFySAe02sYHGlH7H7yJuIKxO0ofS59keVzTtIdiniFG9_jbo6cyTaYHPXxi11BsASjAQfi0vQeSoYh6HU2uG7HZf2jS81G_XouzH7tGZwmXsweZf-J9yelkV1eYWFVJnT0Xo7SkdtIq7Bz46aH9f0i09wvSKY_b6Y6Ka8FnctQelTHox-SsiNE4HKEIc2zgQv-UQ9__LYUuGk5GH47gOav0UFajn7gBKtjL9Il5Uc4HDEH-lmiKLpwoos3YIPfw_zpWC7R27vHBLFWmmz2DvlVKypOxeSJp_0vnNH4pc1Mpf-QEOFotjobX7ZVkixxMaKXPTKMEXfFW_xgnb2VVWzF4ImBt2N_x7sMC2lNtnyCZzqtwpQYVXBXnsvYRbA4bRXE938KK4owhmREmcoNKLw67MwrcqVRuOjep-LYjxU7DF0whQA1qI0kvPdnh7csegHsckMRyDmhXCe5gXdsC6LLdVu-S6gXt9QOJlU-NiIVXQDZ0n0SevYk6CA_VOp6vlHWLG8Q01G_hSNpItMGtP1es3DIgJ8k2wxMX-GjBvVlO7DqQYBZd1IudsU495To6iUe1gewQX7OjWlwr5l411fLXcLZlqQ95cZxsVXkhpGpg6R2l6s_QUJsAMC2Z3Va1PVqe-Kq-BfQOfofrDMF9akETfLZzwgOhL2wmENHvpd1KICKMJBn8OWnTIy2KKZ534T44JA_13kmqR33fWtgTwmonVlGdjYXLtIN4Y_IRuZhcyV_6EW0CtW1Fv4ARH3hIsA80FftiroTXgosHDCDJtYtZy9xIFDpD-bI6hF51aSnIO8OUK0WJ9NllZoJ2-nbvSgQWedfIUE9qHtGn3LlcPDAga9R=w568-h813)

#### No City Found
![](https://lh3.googleusercontent.com/5WNt9U12s87PqMT2mvpTcCkn7ORXwiNhBJfjkVH6uYxESuC1FXQobtZAR-_UyKe7irLxCT1kDa7VU3wYLh1zhqcgCFwHyLlhrqV0NmVpHkgTam8pJNQ0pr2SPk5_R3KoATj0FtXnflAhamuGrbyDWH9Oq-TLNWGeIWG_TSwilrNvEGdYSDHxA2ndSrmz4V98YrTVwgZ3wfovZ4BuRh5ZrYGUtX1HPu0Ijyb_SJRwnSzwx5T1T-zg_SiOg0hkhpwvaPXu5rRj0uzxcB7gJYYpPiUJHxy9tNyjgLOsxkUue3UdzW3FHfsIrm9cuASKD3Hb-9TC1pAnz2ah5jxSz-AfDFwM8uwa8retvxr9kV0_gWLSZ0Zpfp7FTsG5sGWjapvzU64aFXV2epKKefnDMCsRtyZO3HasvejRAiAKZUkjz13n39DlBuOYf2T5c72KZp50vk_lwUuo2hehlYk_vSNYJdFI3W6cux1ptocGiRGUoFnHiRsMqxR6QAyUmAxwrYy1TslRlEsIoa99D5Z0UIpN_yanZcCkQ_EfIPWirbRQ4qtKA2iqdelWreAxfdZB-I9TJ0Znt5sH-c-zsOntYkOVQqOfaStfc-eyBmUZIOcs9OvfUyRmsHVXlWEHnW4lyqsL4gGMP-tOZ1VnwRZqztCzoVtC0E3g2Nvh0bWYC0ZNrXz5IvOEANBu2aF-X_ZZtrKVu8jKHL8ZzsAzTZ9R_tsQ69W9N0e43vCFX9930gyws6bJcVz0B9IowZ0N3ouFfjWu2inVccmC0-I3OV1lNjXdJEJR7ixk1U0qMr_AR6yaU7b4hg9O9d08kgjC5qtDBJwwnI8hkuXlwgH8L6ioewPt5vhaWFua0msLxkRBiQA6-VVwLBnOmF3_OSdctPgFrunojGJNLNDOcNNhjhmUBRxHVh41ycHchK6yxKSyiWiKNbET=w589-h390)

#### Only One City Found
![](https://lh3.googleusercontent.com/DpQPgFi4b7YsszjkG2jK7FlqL6EqMrZrD7h-qTL6A-PPato1AO6eWb-C5f_4Ljr-DJEqgctTuhRxG9Vu0tGCgTm3U43FKKkvkKKAeHZMTkbksWGh5ePHpvJE3X2G_QtbD8HznME0vaQpruBQ68vBkK2CxA6_99kkxaBTLIVThRen3rpizMLc0Y-kv2_eS4PF96mybl0u-Mw38NnPhQH9SUdRVLPkGUfGLsW8fqNCCirImyMQ_V0nLw5BhPYc4cWI0XNeDEqyLAt2zza8CnDRtcDp42xurObXkGvrM1DK2BMyVXlbVNaIqbbpTALJwlBvY5WjjPslDQ8YwKvTIC4Zd4c-s6X_6xNKne98lCDrRsTD-VdFIIWVpKRPh3Ki7S01fUxVlUCi9t63-zfNlIDwMTc2oOGvZTMuocN6yVYtmasLaFT33ZPpafNKd7DcHCrev11uPkooFfMF8kuWwDSMxaNLH9ZtHrzLallWUQuTUupbklFEmaw_YTzY5sp3D93Rv3jJv43qtWN0w-bDaMVpbkU5x12KXCVfIts_5_VNvKyeq1Eiox-dMFYB9JssJ4VVfhWuXJ2U9aucch7aGQVjspNVO8iYmLnhcN_QTpKdBjTHJSMKnazj9dbNMNv6etmf6X6fQzLxatGpNbPl-8zfc-aQwM0_0kj3LWs84e_G72hRCXfbxMH5IfOM3imRN0mjoeNOLOZOEn4vTRfxyJBEjAzbg6sFodNBTNjKye6XtvDoJesRa_rNvKEIAQbwOHu2-esn-X723wWC9cvz-cnX-DNOxzrfp3ZYgT2gYLYF1k_hvUWP-welsYEW-K5lm_9_6Vkip9LSN3O880ifpfCj1Pw_jLcRRUxULf_WtxdgMFtLYp5cpreACOJTCFiDH1KUIkqCcBAXbDR9LRHjk6g7YbMJCs05Su71aVG10YgnEMUD=w610-h273)

#### Wrong User Selection / Asking For Units
![](https://lh3.googleusercontent.com/PKG0YvW5oAnTWcILwpf0la_4M3s9DW1enpU2ieeQzhDTu4wC3qCsXhnfGxSQ6vJ3d4ZnjnP6RQPLQuok5WsJYHwq8G0A2KePuDnYjXa3uHvH8e7hLNuptX3z9hv69D_Nafk7PGYK5sUcFKuLNR79nLNOooA4Nj-9nqav1i16nU8Gwk0lLliX4okjdwqfjb-dlVS22R9CrWpT72IKFCuxLWlIve2X4A-k3-bIip4_T2HmRKL42Xhe5zPYcC2BoI-HD37bDJNZL3oVeKorfqqNZNTfqPy2BSeRafYxfxWHJMnU5n_NFibEEfBpHYAXnMo0DIkPMozZxRyhukF9Zm7Z6ib5O7nibtnJXT0Ld0WYdVYm71dMyYhCh3LBBfwynCUGFIHpX6fiFzwvG18Z_h2cY6f4d4wCbt-adiQpcO7ZvqRPiWFXH_ADA035BXi-elPJbOl8wKx6LYTIA0OpJBOKCGGnbh29Tv157B9Td8OI1_aV-pZ1vuTBLQZ9ZcqgGH0vE61wiDIFXe_BbgDgJHAQVnC58VSrvRd2L7pwE7W6WTqLo_TBRd-gbQOR4AnerKyk_ereppnV0BpL_7HABK3p1bXKT5XKCHwk93JV0HKptllLiDMoXC-cpSc3S6ZOTpNvE_4tqDyG8zoO9_nvSb3JQAKeLaxM7UDn_BWDHEY6S7HhXakYH3Hlq8JgmAlnBHbmlnZ3j4wp8B4QZj_Ott19h-8rcfF5VLdQL9MNAO2ixAhhgoYiw0nqWv4207MgHmucP7Cgh0md6PWAwBsKU9_l3fGG8zjJvsmMPkxOAv88pCt4ETt6BC-15T27aFYSOGKmFLhKgwey8e748yjSd-GORRoEuf9PExvHGLMXmf1FT4f_NLkVYKvi2eMpyLsvJAaYt1QCSoIKRS-_folYic-JLS7gVoOM8u4_jEP-tAWHx1Xj=w657-h654)

#### Displaying Current Weather Using Metric System
![](https://lh3.googleusercontent.com/QJ6wKtgXWouVB-KNOm6u4O8hnkQfZZqNiaYJBSxOuja84znt_8IjgYPYi7LzY2-9u08Jlg6hCOxLRKHtZSKiACl_yox7lchQOKgfz2JVSp102wfPRWvMxbApS05BZTJVkC9-Bugh-czsI6aBCULKO9C_AwnXIsSnEXWSWN4K9ijVj9aRrzhLG_w_g1p5FGdUGe1-NjmQlLmrB2VhYSlSUm_qD4I9Vzy-t-p_TP_DMsPHP4KFjW0xYy7oJIvtrYo0lsIt-lNpGdnVFARIt-PLyK4KkoUK32ebsiD8gPlt8h8spOZQEjZAFs7HJu6s6XJ3O5ibwwgPMRquqopcSrsMzdL9Fv9AXugBbCIAChoWXQhifMtbEFn8FEOHya6GHRhJmf3NvQcKkUBCWEl1yVyHu6Ii1R0bR6TJxJYHhWvBXRWRMuexNKe4-7_OwNUIzogrUsc30m1YkmLYU2Od6Do5S6Cbxj87cpKODqBAu9wYwAUHRkm8BAaSNAiPPFlJJzhkF8qNsiOV40w6Jra_Y3TIEXj_7rd6S316laxjwiP-DANTo9EhKwevZbTSIoRe2JE-sNX_Lg1ec5QVbrR-xETfyFqx68-tE4D12EaHh7h2dNEpfZgq1hMFwWuTyhJEJ2bBNIKHhr4fmsp-N0zoucfL4QG7AUD_EMN4pttkT7LOIvqfbQGz16p0YlD3xhiDjdOwLCwSjzitfnCB12mSxeqyWlITKvzzVN_cSV5PxEm68zPWzvO5mHt7aOkIAhfN8XHUHmwjhv3OEe9XSPQElIRyhQi3Jo2FkeqhoLC1s_NTMf9dze-vm9a5Mnde8N05sZ5ax00033xQPCR-kTYfRqDlvN0Z9BPSNXNT2XBaiDlWh7ZfjDBava3nTfFpcYjATfn6esSYvGwj-8bqXMRC7ryBEw3onmggxX6gUBSPXXVzSvyg=w718-h943)

#### Displaying Current Weather Using Imperial System
![](https://lh3.googleusercontent.com/k289XSJ0DMBkfM89y2IHxMnhdf49lh6yQUtWmrUkHl_sJHvUNXGncNYTwSoMwKdp0SW78wYXuP-OyM3PzBznv9CJGov0t054FaPLYwPB8fpsqKmtx7qzbTwH4B_AdXDfP7s7ikUb-6JazP5UN5Of1N-Enl9fuLqgOjmEk3HwEWtXrJzwxKyJzFgLS9jo4j3F_NKCfOEf2rK0y7sBjRg3goVY1yY9KG1mRFaduzvWX9wNuSpVyyFPLxd1CiPK4jqrWgLqNSI3lyIkl8LL7Gf1D1cbOYbHqGxZ8nQaUXSEJfE5Tp8xcdcdAGQo6KsotipAgd5kI_lXcahRzi53mjXFbNTRI4WNspYER5_i8u9McMdVXnyd33Bafu9dV3Ui948WQAGcE94iXIlHl4QMQJphyqmjdmPmeskkuJdezySYvUtucQzHHf6elM8ygHpYGzpiQ5YNSB0yyz226gSKGY_gZOUw33TpPgghUhx-PfjoDt9VaIEF3LGNP-sN2Q1dN4N4UumxsemojSLSn2wa1oMcs09yLmBU_KUka_yFQ4USr1hL4LgSnjQmC1NrStN-US3xiiY-AxsVPe16tg_qnxa1UX9oXkfg8Q0hqUFSYOelYq4DckJvoHEMU5XoW5QTocWw5JXbkoFuJM9hP1jeaC-mIFEQNUcF1jdy2bhSZX-yiBx9NEFrxVCYIjP6hTLbSspbDczrG77lDho4YVICc_9HCHrmMM_f2oiDogB8AKAF8n8JuEVsln5-EYLcTKTaEKChx7kx59fUyGvwIYzdJZiafKLqfKFcR-C2GDW9U68gKEfA6et1gpjuXld6I8Ld22Qw3BSb1xYlF3GWn0gm560LN7CRQomYbwKe0uyBTeL-OHFHRnkM-rZha1TiwfaTxtx-AK6XAtZqdPpmgIulvbMUnbyWxfBY7TqAjMthBLUkJuHO=w673-h934)

#### Displaying Weather Forecast Using Metric System
![](https://lh3.googleusercontent.com/TLmLj6Yrt2AGHC006jNaCG8v7cmJNmrK3lax9VdNZ79TUxhIVAFo3WEdXrZQ7bFnDt2fDVNa4kkJu1mpjDkW_TljGbZMZecB2wiyRdE-oZaYu5LBeYod3xh5wiQgna3Y4NtT628TWpcYiaMzOf7YXNCMHC82058xMH7G72GPiIkglUZ8vs4J6yOcWepYi8NkqiNFLdGzZBGW4jmuJRyHnDh8XAcnwK5b4qcN-VaXq1VLGFIPLe9KeDQ0TFPU8IjXURYTIO5ZFBfWW6735xGSPzQbYsR0hzeXTCG4oSJnHWh53hCum4gxALxNU6qVriSROW72d1K9_Egfq1h5dt_-kcUzBIA4EojdnsjImaS1tAtcfOeq8xzkwd_I-PmJUFHtXRhChhU3SUspJoaiVS3ETPrJY-59yaJVDUF62C8HU2lG7jd6cixcga6Og86-ZKQiWySoC9Vf_oywWecCwVSsguoaYvNtt8GVBm3XFCKsRmP2Yb466081mmOePWATnDUXjFcVzyWzDi5kOr6LUC9k5d28png49nzgqIYLrNSwZbG8R6CVgplD1kbWjrmvL7v3YLDTJ9GVDw1EQggW-vwS4wwe_wvU5d187swVxhT0hzOCTUVbceRUycBWbmcg-V9DZwhNfZFvJJj1hmJ_Sq56aCYtbgYnQEjamSVYJ5qMT47610L8Bx7dx9TYQUDAEHfa9tSDks-IF17ZA9pZo2Ub7CHuyZVJzSexnr0GWaS9c8SVYkTXkiwmOhBzy1547jCj3fIRcv5ER9n5neMCrOLXgvjhEdZI_exUZU86peOOTy6IQUYTAHOZ31LlUK5SKQUSX5xeJJzVsJ8a5u0MEUKuTQL-6RENSmAPcQxhi1GDqgXG3jT8Q9Fw8CvUHmlOOE7ZEeeYqx7lNKhJkz3RsTk3621nuWLjhg2t95ou7OyvFSLw=w502-h909)

#### Displaying Weather Forecast Using Imperial System
![](https://lh3.googleusercontent.com/LZupkoFvvM7TV3VaqHwCc35asOM4EUgfJY20LA-Dr2sNcAwWz6H1NVWeCEHg4tfwyqyOkhwK27tLkUnoD-uGwd6xjxPF21laXZUulT9h-iQIPwLuL41f5tU8LqQdzO8NKJMP-ZpTd6ficaUfKEfsfd5V50b95HlBNqSo8vzogLLR807PvW_HVXx_GlBSDh7QKsljxKrvXFU2ZV_SiorHyczxfJCL3Va_x8kUr1wOcyPFr5o7dmM0hG20d2rISvS9uNoJliUSKkyBi1Nqc_v21FVB6dpKP9RLAoYtwbtbzTwbQkwcehWZLyOf4KjhBRqmdeHqHjeAl6byNzSDKS-1DgCGr6TrFQx7kA-rsS9AVrejCkylaj1CgafkoLTAogXF6kEKRpbeqSXCp2lCMVVmunRpH4TfNXYCWW63ZhOpLigmsSZZKjQ7suBIkkkxp4Z-ASfMffh4jcZRvITmdyuiKaUeoCfMXzHJSsTZ2h7_YKvNTyCJX6DHx-VzZKEOjC7rc79P1FrepH2802REVmdhZm6G0H0OJVDNC5iJ_G5bGAkSgqt1A2MtT42_6EfarYdpNd6Yka5NRXJ-ow1BKyqzl3MRW3L0dcuf0xpbQ3eOgZ3MsHd9KNkYl4c_urVGAOgdwwBbJwXfjgia0sXrQX4NFTwhSq0na3ppoQ_Kgu2puMjRcNZtcvC0S_ZRtz1ZCYIAjU8b9JGk3q5hIcAX5m4pxmVkyZRdngk2MdHBhNzgQ9iPJ7ymcbeLjggmuHg0JK6CfKPrGcKT89hWD5YB6adNmax7T6u5v_mQ8te2D0VLrUZ9sinRk9zX6cdWl44p7AFXsTtRJY7WUhR6crdRz_gkbqVHDk8KLPgf0z7R_aO_BrEIBKBRCAGKXIWUKpZI0dQNDPAzZds72Lof1hsf7l8QBg__c6Rfc0sKHZVB5bX8YveM=w510-h915)
