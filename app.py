from flask import Flask, render_template, request
from datetime import datetime, timedelta
import requests, random

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_weather():
    now = datetime.now()
    current_time = now.strftime('%H:%M')
    current_date = now.strftime('%A, %B %d')
    current_year = now.year

    city = request.form.get('city')
    api_key = '8a3eaa8c7ee92c32df16c38ddd11dc64'
    
    weather_data = None
    forecast = None
    error_message = None

    outdoor_activities = [
    "Hiking or Nature Walks",
    "Picnics",
    "Cycling",
    "Photography",
    "Beach Day",
    "Outdoor Sports",
    "Stargazing",
    "Outdoor Yoga or Meditation",
    "Boating or Kayaking",
    "Barbecue or Grilling",
    "Camping",
    "Gardening",
    "Sightseeing or Exploring New Places",
    "Fishing",
    "Outdoor Workout"
]

    indoor_activities = [
    "Reading Books",
    "Board Games",
    "Watching Movies or TV Shows",
    "Cooking or Baking",
    "Indoor Yoga or Meditation",
    "Puzzles or Brain Teasers",
    "Video Games",
    "Arts and Crafts",
    "Listening to Music or Podcasts",
    "Writing or Journaling",
    "Learning a New Skill or Hobby",
    "Cleaning and Organizing",
    "Home Workouts",
    "Indoor Photography",
    "Building DIY Projects",
    "Online Classes or Courses"
]

    if city:
        # Fetch current weather data
        current_weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        try:
            current_response = requests.get(current_weather_url)
            current_response.raise_for_status()
            current_weather_data = current_response.json()

            if current_weather_data.get('cod') == 200:
                main = current_weather_data['main']
                weather_data = {
                    'city': city,
                    'temperature_celsius': round(main['temp']),
                    'temperature_fahrenheit': round((main['temp'] * 9/5) + 32),
                    'feels_like_celsius': round(main.get('feels_like')),
                    'feels_like_fahrenheit': round((main.get('feels_like') * 9/5) + 32),
                    'weather_icon': current_weather_data['weather'][0]['icon'],
                    'wind_speed': round(current_weather_data['wind']['speed']),
                    'visibility': round(current_weather_data['visibility'] / 1000),  # Convert to km
                    'humidity': main['humidity'],
                    'pressure': main['pressure'],
                    'weather_desc': current_weather_data['weather'][0]['description']
                }

                # Fetch 5-day forecast data
                forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
                forecast_response = requests.get(forecast_url)
                forecast_response.raise_for_status()
                forecast_data = forecast_response.json()

                # Prepare 5-day forecast
                forecast = []
                current_date = datetime.now().date()
                for item in forecast_data['list']:
                    forecast_date = datetime.fromtimestamp(item['dt']).date()
                    if forecast_date > current_date and len(forecast) < 5:
                        weather_condition = item['weather'][0]['main'].lower()
                        if 'clear' in weather_condition or 'sunny' in weather_condition:
                            activity = "Great day for outdoor activities!"
                            recommended_activities = random.sample(outdoor_activities,2)
                            recommended_activities = ", ".join(recommended_activities)
                        elif 'cloud' in weather_condition or 'overcast' in weather_condition:
                            activity = "Consider indoor activities today."
                            recommended_activities = random.sample(indoor_activities,2)
                            recommended_activities = ", ".join(recommended_activities)
                        elif 'rain' in weather_condition or 'thunderstorm' in weather_condition:
                            activity = "Consider indoor activities today."
                            recommended_activities = recommended_activities = random.sample(indoor_activities,2)
                            recommended_activities = ", ".join(recommended_activities)
                        else:
                            activity = "Check the weather before planning activities."
                        
                        forecast.append({
                            'day': forecast_date.strftime('%a'),  # Abbreviated day name
                            'date': forecast_date.strftime('%m/%d'),  # Date in MM/DD format
                            'icon': item['weather'][0]['icon'],
                            'description': item['weather'][0]['description'],
                            'temp_c': round(item['main']['temp']),
                            'temp_f': round((item['main']['temp'] * 9/5) + 32),
                            'activity': activity,
                            'recommended_activities': recommended_activities
                        })
                        current_date = forecast_date

            else:
                error_message = f"Error: {current_weather_data.get('message', 'Unknown error occurred')}"

        except requests.RequestException as e:
            error_message = f"Error fetching weather data: {str(e)}"

    return render_template('index.html', 
                           current_year=current_year,
                           current_date=current_date,
                           current_time=current_time,
                           weather=weather_data,
                           forecast=forecast,
                           error_message=error_message)

@app.route('/schedule_event', methods=['GET', 'POST'])
def schedule_event():
    schedule_date = request.args.get('date')  # Get the date for scheduling from query parameter
    return render_template('schedule_event.html', schedule_date=schedule_date)

if __name__ == '__main__':
    app.run(debug=True)