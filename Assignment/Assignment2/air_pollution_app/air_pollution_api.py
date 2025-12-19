import requests
import json
import os
from dotenv import load_dotenv
"""
Get current air pollution data for a city name using openweather
"""
load_dotenv()

def current_air_condition_of_city(city):
    """
    Get the air pollution of city by the getting lon and lat of a city first then 
    by that co-ordinates get the data of pollution
    """

    api_key = os.getenv("OPEN_WEATHER_API")
    BASE_URL_AIR = "http://api.openweathermap.org/data/2.5/air_pollution"
    BASE_URL_LOC = "http://api.openweathermap.org/geo/1.0/direct"
    # 1) Getting lat and lon for city
    geographic_url = f"{BASE_URL_LOC}?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(geographic_url)
        response.raise_for_status()
        geo_data = response.json()
        if not geo_data:
            print(f"Location not found for '{city}'.")
            return None

        lat = geo_data[0].get("lat")
        lon = geo_data[0].get("lon")
        if lat is None or lon is None:
            print("Geocoding response missing lat/lon.")
            return None
        
        # 2) Getting air pollution of a city
        pollution_url =f"{BASE_URL_AIR}?lat={lat}&lon={lon}&appid={api_key}"
        pol_resp = requests.get(pollution_url, timeout=10)
        pol_resp.raise_for_status()
        pol_data = pol_resp.json()
    
        entries = pol_data.get("list")
        if not entries or len(entries) == 0:
            print("No air pollution data available for this location.")
            return None

        entry0 = entries[0]
        aqi = entry0.get("main", {}).get("aqi")
        components = entry0.get("components", {})

        aqi_map = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        return {
            "city": city,
            "lat": lat,
            "lon": lon,
            "aqi": int(aqi) if aqi is not None else None,
            "aqi_text": aqi_map.get(aqi, "Unknown"),
            "components": components,
            "raw": pol_data
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
    except json.JSONDecodeError:
        print("Error decoding JSON response from the API.")
    return None

if __name__=="__main__":
    city =input("Enter the city name: ")
    data = current_air_condition_of_city(city)
    print(data)