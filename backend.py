from flask import Flask, jsonify, render_template, request
import requests
app = Flask(__name__)
WEATHER_API_KEY = "aaeb2544f95d036fc988970a67433c42"
@app.route('/')
# Frontend route
def frontend():
    return render_template('index.html')
@app.route('/get_data') 
# Backend route
def get_data():
    lat = request.args.get('lat', 28.9956)
    lon = request.args.get('lon', 77.0110)
    try:
        # Weather
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric"
        weather_data = requests.get(weather_url).json()
        #Aqi
        aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
        aqi_data = requests.get(aqi_url).json()
        aqi_value = aqi_data["list"][0]["main"]["aqi"]
        conversion_map = {1: (0, 50, "Good 😊"),
                         2: (51, 100, "Fair 🙂"),
                         3: (101, 150, "Moderate 😐"),
                         4: (151, 200, "Poor 😷"),
                         5: (201, 500, "Very Poor 🤢")}
        aqi_min, aqi_max, aqi_text = conversion_map.get(aqi_value, (0, 0, "Unknown"))
        aqi_estimate = (aqi_min + aqi_max) // 2
        #display data
        result = {"city": weather_data.get("name", "Unknown"),
            "temp": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "condition": weather_data["weather"][0]["description"].title(),
            "aqi": aqi_estimate,
            "aqi_desc": aqi_text}
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)







