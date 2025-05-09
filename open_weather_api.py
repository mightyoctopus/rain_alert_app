import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

#------------------------------------------------ OPEN WEATHER API ------------------------------------------------#
API_KEY = os.getenv("API_KEY")
OWM_Endpoint = os.getenv("OWM_Endpoint")

weather_params = {
    "lat": "37.609892",
    "lon": "126.731146",
    "appid": API_KEY,
    "cnt": 5,
}

def check_weather():
    weather_response = requests.get(OWM_Endpoint, params=weather_params)
    # print(response.status_code)
    weather_response.raise_for_status()
    weather_data = weather_response.json()

    for hour_data in weather_data["list"]:
        condition_code = hour_data["weather"][0]["id"]

        if condition_code <= 700:
            return True
        else:
            return False


