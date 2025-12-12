import air_pollution_api as apa
"""Main file for excution of app"""
if __name__=="__main__":
    city = input("Enter city name for air condition: ")
    data = apa.current_air_condition_of_city(city)
    print("City:",data["city"])
    print("Longitude:", data["lon"], " and latitude: ", data["lat"])
    print("AQI: ",data["aqi_text"])
    print("Components:\n")
    for k, v in data["components"].items():
        print(f" {k}: {v}")
    print()