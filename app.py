from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)
WEATHER_API_KEY = "d5ece5648ce79a1f893f16b132495d53"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    lat = request.args.get('lat', 28.9956)
    lon = request.args.get('lon', 77.0110)

    try:
        # Weather API
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        weather_data = requests.get(weather_url, timeout=10).json()

        # AQI API
        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        aqi_data = requests.get(aqi_url, timeout=10).json()

        # Safe extraction with defaults
        city = weather_data.get("name", "Unknown")
        temp = weather_data.get("main", {}).get("temp", "--")
        humidity = weather_data.get("main", {}).get("humidity", "--")
        condition = weather_data.get("weather", [{}])[0].get("description", "--").title()

        # AQI conversion
        aqi_value = 0
        if "list" in aqi_data and len(aqi_data["list"]) > 0:
            aqi_value = aqi_data["list"][0]["main"].get("aqi", 0)

        conversion_map = {
            1: (0, 50, "Good 😊"),
            2: (51, 100, "Fair 🙂"),
            3: (101, 150, "Moderate 😐"),
            4: (151, 200, "Poor 😷"),
            5: (201, 500, "Very Poor 🤢")
        }
        aqi_min, aqi_max, aqi_text = conversion_map.get(aqi_value, (0, 0, "Unknown"))
        aqi_estimate = (aqi_min + aqi_max) // 2

        return jsonify({
            "city": city,
            "temp": temp,
            "humidity": humidity,
            "condition": condition,
            "aqi": aqi_estimate,
            "aqi_desc": aqi_text
        })

    except Exception as e:
        return jsonify({
            "city": "--",
            "temp": "--",
            "humidity": "--",
            "condition": "--",
            "aqi": "--",
            "aqi_desc": "Error"
        })

if __name__ == '__main__':
    app.run(debug=True)







