import os
import json
import requests

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")


# to check Paris current weather => https://www.google.com/search?q=current+weather+forecast+in+Pariss&sca_esv=578154760&rlz=1C5CHFA_enFR894FR895&sxsrf=AM9HkKl9Zr9kHBbMZWlWtK0wYQTSf3bv4A%3A1698759926514&ei=9gRBZaLvHrGokdUPsbiq0As&ved=0ahUKEwiiwunvtaCCAxUxVKQEHTGcCroQ4dUDCBE&uact=5&oq=current+weather+forecast+in+Pariss&gs_lp=Egxnd3Mtd2l6LXNlcnAiImN1cnJlbnQgd2VhdGhlciBmb3JlY2FzdCBpbiBQYXJpc3MyChAhGKABGMMEGAoyChAhGKABGMMEGAoyChAhGKABGMMEGApI3AdQ1QFYzARwAXgBkAEAmAFWoAHnAaoBATO4AQPIAQD4AQHCAgoQABhHGNYEGLADwgIFEAAYogTiAwQYACBBiAYBkAYI&sclient=gws-wiz-serp


def kelvin_to_celsius(kelvin):
    return json.dumps(round(kelvin - 273.15))


def kelvin_to_fahrenheit(kelvin):
    return round((kelvin - 273.15) * 9 / 5 + 32, 2)

# util function that gets the coordinates of a given location name
def geo_code(location):
    loc = location.split(",")[0]
    url = (
        f"http://api.openweathermap.org/geo/1.0/direct?q={loc}&appid={WEATHER_API_KEY}"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()
        coordinates = response.json()
        lat = coordinates[0].get("lat")
        lon = coordinates[0].get("lon")
        return lat, lon

    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None, None

# JSON response example:
# {
#   "coord": {
#     "lon": 10.99,
#     "lat": 44.34
#   },
#   "weather": [
#     {
#       "id": 501,
#       "main": "Rain",
#       "description": "moderate rain",
#       "icon": "10d"
#     }
#   ],
#   "base": "stations",
#   "main": {
#     "temp": 298.48,
#     "feels_like": 298.74,
#     "temp_min": 297.56,
#     "temp_max": 300.05,
#     "pressure": 1015,
#     "humidity": 64,
#     "sea_level": 1015,
#     "grnd_level": 933
#   },
#   "visibility": 10000,
#   "wind": {
#     "speed": 0.62,
#     "deg": 349,
#     "gust": 1.18
#   },
#   "rain": {
#     "1h": 3.16
#   },
#   "clouds": {
#     "all": 100
#   },
#   "dt": 1661870592,
#   "sys": {
#     "type": 2,
#     "id": 2075663,
#     "country": "IT",
#     "sunrise": 1661834187,
#     "sunset": 1661882248
#   },
#   "timezone": 7200,
#   "id": 3163858,
#   "name": "Zocca",
#   "cod": 200
# }                        
                        
def get_current_weather(location, unit="celsius"):
    lat, lon = geo_code(location)

    if lat is None or lon is None:
        print("Failed to get location coordinates.")
        return

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        current_temp = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]

        weather_info = {
            "location": location,
            "temperature": kelvin_to_celsius(current_temp)
            if unit == "celsius"
            else kelvin_to_fahrenheit(current_temp),
            "unit": unit,
            "forecast": description,
        }

        # make sure to convert to stringified json object
        return json.dumps(weather_info)

    except requests.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return
