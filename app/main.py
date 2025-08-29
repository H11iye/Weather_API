from flask import Flask, jsonify, request
import requests, os # Import os to access environment variables for API key management 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
API_KEY = os.getenv('WEATHER_API_KEY')  # Fetch the API key from environment variables
if not API_KEY:
    raise ValueError("No API key found. Please set the WEATHER_API_KEY environment variable.")


BASE_URL = "http://api.openweathermap.org/data/2.5/weather" 

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Paris')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500
    

    data = response.json()
    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description']
    }
    return jsonify(weather_info)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)