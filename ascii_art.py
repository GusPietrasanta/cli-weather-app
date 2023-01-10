from pyfiglet import Figlet
import emoji
import random

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

"""
print("\n\n")
for _ in range(emojis_to_print):
    print(emoji.emojize(random.choice(emojis_list)), end="  ")

print()
print(figlet.renderText(text))

for _ in range(emojis_to_print):
    print(emoji.emojize(random.choice(emojis_list)), end="  ")
print("\n\n")
"""

string_to_return = ""

string_to_return += "\n\n"
for _ in range(emojis_to_print):
    string_to_return += emoji.emojize(random.choice(emojis_list)) + "  "
string_to_return += "\n"
string_to_return += figlet.renderText(text)
for _ in range(emojis_to_print):
    string_to_return += emoji.emojize(random.choice(emojis_list)) + "  "
string_to_return += "\n\n"

print(string_to_return)
