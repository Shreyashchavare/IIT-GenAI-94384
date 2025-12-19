import requests
import json
import os
from dotenv import load_dotenv
"""
 Create a weather app that takes city input and displays forecast
"""
load_dotenv()
def current_weather_of_city(city):
    """
    returns the data of weather of the city by input
    """
    api_key = os.getenv("OPEN_WEATHER_API")
    BASE_URL ="https://api.openweathermap.org/data/2.5/weather" 
    complete_weather_url = f"{BASE_URL}?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(complete_weather_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response from the API.")
    return None

if __name__ == "__main__":
    city = input("Enter city name: ")
    data = current_weather_of_city(city)
    print(data)
    # print(f"Tempreature: ", data["main"]["temp"])
    # print(f"Humidity: ", data["main"]["temp"])