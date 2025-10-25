from dotenv import load_dotenv
from flask import Flask, jsonify, request
from datetime import datetime
from weather_service import WeatherService

# Load environment variables from .env
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Initialize the WeatherService (calls OpenWeather API)
service = WeatherService()

@app.get("/health")
def health():
    """Simple health check endpoint."""
    return jsonify(status="ok", ts=datetime.utcnow().isoformat() + "Z")

@app.get("/v1/weather")
def get_weather():
    """Fetch real weather data from OpenWeather API."""
    city = request.args.get("city", "").strip()
    units = request.args.get("units", "metric")  # can be 'metric' or 'imperial'

    if not city:
        return jsonify(error="Missing 'city' parameter"), 400

    # Fetch data from the weather service
    data = service.get_weather(city, units=units)

    # Handle error cases
    if "error" in data:
        code = 404 if data.get("error") == "City not found" else 502
        return jsonify(data), code

    # Add timestamp and return
    data["requested_at"] = datetime.utcnow().isoformat() + "Z"
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
