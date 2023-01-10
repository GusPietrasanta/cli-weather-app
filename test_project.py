from project import (
    deg_to_compass,
    get_country_name_from_code,
    calculate_visibility,
    get_emoji_from_id,
)


def test_deg_to_compass():
    assert deg_to_compass(360) == "N"
    assert deg_to_compass(0) == "N"
    assert deg_to_compass(90) == "E"
    assert deg_to_compass(180) == "S"
    assert deg_to_compass(270) == "W"
    assert deg_to_compass(200) == "SSW"
    assert deg_to_compass(160) == "SSE"


def test_get_country_name_from_code():
    assert get_country_name_from_code("AR") == "Argentina"
    assert get_country_name_from_code("AU") == "Australia"
    assert get_country_name_from_code("US") == "United States"
    assert get_country_name_from_code("ZM") == "Zambia"
    assert get_country_name_from_code("FR") == "France"


def test_calculate_visibility():
    assert calculate_visibility(10000, "metric") == 10.00
    assert calculate_visibility(10000, "imperial") == 10.00
    assert calculate_visibility(5000, "metric") == 5.00
    assert calculate_visibility(5000, "imperial") == 3.11
    assert calculate_visibility(2500, "metric") == 2.50
    assert calculate_visibility(2500, "imperial") == 1.55
    assert calculate_visibility(0, "metric") == 0.00
    assert calculate_visibility(0, "imperial") == 0.00


def test_get_emoji_from_id():
    assert (get_emoji_from_id("212", 1673327846, 1673293336, 1673344973)
            == ":cloud_with_lightning_and_rain:")
    assert (get_emoji_from_id("311", 1673327846, 1673293336, 1673344973)
            == ":cloud_with_rain:")
    assert (get_emoji_from_id("520", 1673327846, 1673293336, 1673344973)
            == ":cloud_with_rain:")
    assert (get_emoji_from_id("616", 1673327846, 1673293336, 1673344973)
            == ":snowflake:")
    assert (get_emoji_from_id("762", 1673327846, 1673293336, 1673344973)
            == ":fog:")
    assert (get_emoji_from_id("800", 1673327846, 1673293336, 1673344973)
            == ":sun:")
    assert (get_emoji_from_id("800", 1673338061, 1673340689, 1673392197)
            == ":last_quarter_moon:")
    assert (get_emoji_from_id("803", 1673327846, 1673293336, 1673344973)
            == ":cloud:")
    assert (get_emoji_from_id("802", 1673338061, 1673340689, 1673392197)
            == ":cloud:")
