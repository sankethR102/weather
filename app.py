from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)

# Load .env file
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    city = request.json['city']
    url = f"https://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=3"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({'error': 'City not found'}), 404

    data = response.json()

    # Current weather
    current = {
    'location': f"{data['location']['name']}, {data['location']['country']}",
    'temp': data['current']['temp_c'],
    'condition': data['current']['condition']['text'],
    'icon': data['current']['condition']['icon'],
    'wind': data['current']['wind_kph'],
    'humidity': data['current']['humidity'],
    'pressure': data['current']['pressure_mb'],
    'sunrise': data['forecast']['forecastday'][0]['astro']['sunrise'],
    'sunset': data['forecast']['forecastday'][0]['astro']['sunset']
}


    # 3-day forecast
    forecast_days = []
    for day in data['forecast']['forecastday']:
        day_info = {
            'date': day['date'],
            'avg_temp': day['day']['avgtemp_c'],
            'condition': day['day']['condition']['text'],
            'icon': day['day']['condition']['icon']
        }
        forecast_days.append(day_info)

    # Hourly forecast for graph (today only)
    hourly = data['forecast']['forecastday'][0]['hour']
    graph_data = {
        'times': [h['time'].split()[-1] for h in hourly],  # get HH:MM
        'temps': [h['temp_c'] for h in hourly]
    }

    return jsonify({
        'current': current,
        'forecast': forecast_days,
        'graph': graph_data
    })


if __name__ == '__main__':
    app.run(debug=True)
