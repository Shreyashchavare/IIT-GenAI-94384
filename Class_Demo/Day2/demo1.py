import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPEN_WEATHER_API")
city = input("Enter city: ")
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
response = requests.get(url)
weather = response.json()
print(weather)