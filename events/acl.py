import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY

import json


def find_pictures(search_term):
    pexel_url = "https://api.pexels.com/v1/search?query=" + search_term
    headers = {"Authorization": PEXELS_API_KEY}

    response = requests.get(pexel_url, headers=headers)

    data = json.loads(response.content)

    photos = data["photos"]

    # you could pick one photo at this state
    # photo = photos[0]

    # return Python dictionary that can be used by your view code
    return photos


def get_weather_data(city, state):
    url = (
        "http://api.openweathermap.org/geo/1.0/direct?q="
        + city
        + state
        + ",US&limit=5&appid="
        + OPEN_WEATHER_API_KEY
    )

    response = requests.get(url)

    data = json.loads(response.content)

    if len[data] != 0:
        one_data_point = data[0]
        lat = one_data_point["lat"]
        lon = one_data_point["lon"]

    else:
        return None

    weather_url = (
        "https://api.openweathermap.org/data/2.5/weather?lat="
        + lat
        + "&lon="
        + lon
        + OPEN_WEATHER_API_KEY
    )
