from flask import Flask, jsonify, request
import requests, os # Import os to access environment variables for API key management 

app = Flask(__name__)
API_KEY = os.getenv('WEATHER_API_KEY')  # Fetch the API key from environment variables
BASE_URL = "http://api.openweathermap.org/data/2.5/weather" 

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": "City not found or API error"}), response.status_code

    data = response.json()
    weather_info = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description']
    }
    return jsonify(weather_info)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500)