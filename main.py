import datetime
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

APIKEY = open("APIKEY", 'r').read()


def return_location(city_name: str):
    params = {
        'q': city_name,
        'appid': APIKEY
    }
    data = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params).json()['coord']
    return data['lat'], data['lon']


def weather_forcast(lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
        'exclude': 'minutely,hourly,alerts,current',
        'units': 'metric',
        'appid': APIKEY
    }
    data = requests.get('https://api.openweathermap.org/data/3.0/onecall', params=params).json()
    return data['daily']


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        lat, lon = return_location(request.form['city'])
        weather_info = []
        for daily_info in weather_forcast(lat, lon)[:6]:
            weather_info.append({
                'dt': datetime.datetime.utcfromtimestamp(daily_info['dt']).strftime('%A'),
                'day': datetime.datetime.utcfromtimestamp(daily_info['dt']).strftime('%d'),
                'year': datetime.datetime.utcfromtimestamp(daily_info['dt']).strftime('%b'),
                'icon': f"https://openweathermap.org/img/wn/{daily_info['weather'][0]['icon']}@2x.png",
                'main': daily_info['weather'][0]['main'],
                'max_temp': daily_info['temp']['max'],
                'min_temp': daily_info['temp']['min'],
                'summary': daily_info['summary'],
                'description': daily_info['weather'][0]['description'],
            })
        return render_template('index.html', weathers=weather_info)
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
