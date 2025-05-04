import os
from configparser import ConfigParser

import requests

class ApiHelper:
    def __init__(self):
        config = ConfigParser()

        # Build the absolute path to config.ini
        config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))
        print(f"Loading config from: {config_path}")  # Debug print

        config.read(config_path)

        if "API" not in config or "API_KEY" not in config["API"]:
            raise ValueError(f"'API_KEY' not found in config file at {config_path}")

        self.BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
        self.API_KEY = config["API"]["API_KEY"]

    def get_current_weather(self, city):
        url = f"{self.BASE_URL}?q={city}&appid={self.API_KEY}"
        print(f"Requesting URL: {url}")
        response = requests.get(url)
        return response

    def get_weather_by_city_id(self, city_id):
        url = f"{self.BASE_URL}?id={city_id}&appid={self.API_KEY}"
        response = requests.get(url)
        return response

