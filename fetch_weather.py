import os
import requests

# Store your API key in an environment variable for security
API_KEY = os.getenv("OPENWEATHER_API_KEY")   # Set this in your environment
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# coordinates
latitude = 17.387140
longitude = 78.491684

# Make the API request
if API_KEY:
    response = requests.get(
        BASE_URL,
        params={
            "lat": latitude,
            "lon": longitude,
            "appid": API_KEY,
            "units": "metric"
        }
    )
    if response.status_code == 200:
        data = response.json()
         # Extract temperature, humidity, and pressure
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        print(f"Temperature in Celsius: {temperature}°C")
        print(f"Humidity: {humidity}%")
        print(f"Pressure: {pressure} hPa")
    else:
        print(f"Error: Unable to fetch weather data. Status code: {response.status_code}")
else:
    print("Error: API key not found. Please set the OPENWEATHER_API_KEY environment variable.")