from flask import Flask, jsonify, request
from datetime import datetime
from weather_service import WeatherService

app = Flask(__name__)
service = WeatherService()

@app.get("/health")
def health():
    return jsonify(status="ok", ts=datetime.utcnow().isoformat() + "Z")

@app.get("/v1/weather")
def get_weather():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify(error="Missing 'city' parameter"), 400
    try:
        data = service.get_weather(city)
    except KeyError:
        return jsonify(error=f"No data for {city.strip().lower()}"), 404
    data["requested_at"] = datetime.utcnow().isoformat() + "Z"
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
