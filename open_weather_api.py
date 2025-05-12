import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

#------------------------------------------------ OPEN WEATHER API ------------------------------------------------#
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OWM_Endpoint = os.getenv("OWM_Endpoint")

weather_params = {
    "lat": "37.609892",
    "lon": "126.731146",
    "appid": WEATHER_API_KEY,
    "cnt": 5,
}

def check_weather():
    weather_response = requests.get(OWM_Endpoint, params=weather_params)
    weather_response.raise_for_status()
    weather_data = weather_response.json()
    print(weather_data)

    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]

        return True if condition_code < 700 else False

print(check_weather())

