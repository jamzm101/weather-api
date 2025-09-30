class WeatherService:
    """Pure logic: look up a city and return a normalized record."""
    def __init__(self, seed=None):
        self._data = seed or {
            "lima": {"temp_c": 19, "condition": "Cloudy"},
            "cusco": {"temp_c": 12, "condition": "Sunny"},
            "san diego": {"temp_c": 22, "condition": "Clear"},
        }

    def get_weather(self, city: str):
        key = (city or "").strip().lower()
        if key not in self._data:
            raise KeyError(key)
        rec = self._data[key]
        return {
            "city": key.title(),
            "temperature_c": rec["temp_c"],
            "condition": rec["condition"],
        }
