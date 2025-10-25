# weather_service.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads .env in project root

class WeatherService:
    def __init__(self):
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        if not self.api_key:
            raise KeyError("OPENWEATHER_API_KEY not set")

    def get_weather(self, city: str, units: str = "metric") -> dict:
        """
        Call OpenWeather /weather and return a normalized dict.
        units: 'metric' (°C) or 'imperial' (°F)
        """
        if not city:
            return {"error": "Missing city"}

        r = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": self.api_key, "units": units},
            timeout=10,
        )

        if r.status_code == 404:
            return {"error": "City not found", "detail": r.text}
        try:
            r.raise_for_status()
        except Exception:
            return {"error": "Upstream error", "status": r.status_code, "detail": r.text[:300]}

        d = r.json()
        temp = d.get("main", {}).get("temp")
        out = {
            "city": d.get("name"),
            "country": d.get("sys", {}).get("country"),
            "humidity": d.get("main", {}).get("humidity"),
            "conditions": ", ".join([w["description"] for w in d.get("weather", [])]),
            "wind_speed": d.get("wind", {}).get("speed"),
            "units": units,
        }
        if units == "metric":
            out["temp_c"] = temp
        else:
            out["temp_f"] = temp
        return out
