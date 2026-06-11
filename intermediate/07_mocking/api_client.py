import urllib.request
import json
import os


class WeatherClient:
    BASE_URL = "https://api.weather.example.com"

    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("WEATHER_API_KEY", "demo")

    def get_temperature(self, city: str) -> float:
        url = f"{self.BASE_URL}/temperature?city={city}&key={self.api_key}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        return data["temperature"]

    def get_forecast(self, city: str, days: int = 3) -> list:
        url = f"{self.BASE_URL}/forecast?city={city}&days={days}&key={self.api_key}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        return data["forecast"]

    def is_rainy(self, city: str) -> bool:
        url = f"{self.BASE_URL}/conditions?city={city}&key={self.api_key}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
        return data.get("condition") == "rain"


class NotificationService:
    def __init__(self, weather_client: WeatherClient):
        self.client = weather_client
        self.sent = []

    def notify_if_cold(self, city: str, threshold: float = 10.0) -> bool:
        temp = self.client.get_temperature(city)
        if temp < threshold:
            message = f"Cold alert: {city} is {temp}°C"
            self.sent.append(message)
            return True
        return False

    def daily_summary(self, city: str) -> dict:
        temp = self.client.get_temperature(city)
        rainy = self.client.is_rainy(city)
        return {"city": city, "temp": temp, "rainy": rainy}
