# weather_service.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env in project root

class WeatherService:
    def __init__(self):
        # CHANGED: use WeatherAPI.com key name
        self.api_key = os.getenv("WEATHERAPI_KEY")
        if not self.api_key:
            raise KeyError("WEATHERAPI_KEY not set")

        # CHANGED: WeatherAPI base URL
        self.base = "https://api.weatherapi.com/v1"

    def get_weather(self, city: str, units: str = "metric") -> dict:
        """
        Call WeatherAPI /current.json and return a normalized dict.
        units: 'metric' (°C) or 'imperial' (°F)
        """
        if not city:
            return {"error": "Missing city"}

        try:
            r = requests.get(
                f"{self.base}/current.json",
                params={"key": self.api_key, "q": city, "aqi": "no"},
                timeout=10,
            )
        except requests.RequestException as e:
            return {"error": "Upstream error", "detail": str(e)}

        if r.status_code == 401:
            return {"error": "Unauthorized (401) – check WEATHERAPI_KEY", "detail": r.text}
        if r.status_code == 404:
            return {"error": "City not found", "detail": r.text}

        try:
            r.raise_for_status()
        except Exception:
            return {"error": "Upstream error", "status": r.status_code, "detail": r.text[:300]}

        d = r.json()

        # WeatherAPI returns both C and F; normalize to your 'units' flag
        temp_c = d["current"]["temp_c"]
        temp_f = d["current"]["temp_f"]
        temp = temp_c if units == "metric" else temp_f

        return {
            "city": d["location"]["name"],
            "country": d["location"]["country"],
            "coords": {"lat": d["location"]["lat"], "lon": d["location"]["lon"]},
            "humidity": d["current"]["humidity"],
            "conditions": d["current"]["condition"]["text"],
            "wind_speed_mph": d["current"]["wind_mph"],
            "units": units,
            "temp_c": temp_c,
            "temp_f": temp_f,
            "temp": temp,  # convenience: current temp in requested units
            "raw": d,      # keep for debugging; remove later if you want
        }
