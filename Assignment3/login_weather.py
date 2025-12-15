import streamlit as st
import pandas as pd 
from dotenv import load_dotenv
import os
import requests
from datetime import datetime


def user_login(username, password):
    """
    User login by verification of username and password
    return: True/False

    """
    return username == username and password == password

def get_weather_city(city):
    """
    Finds weather based on city input

    args: city

    return: Tempreature, 
    Feels like, 
    Min Tempreature, 
    Max Tempreature, 
    Pressure,
    Humidity,
    Sunrise,
    Sunset
    """
    try:
        load_dotenv()
        api_key = os.getenv("OPEN_WEATHER_API")
        if not api_key:
            st.error("API key not found. Check your .env file.")
            return None

        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{BASE_URL}q={city}&appid={api_key}&units=metric"
        response = requests.get(complete_url)
        if response.status_code != 200:
            st.error(data.get("message", "Failed to fetch weather"))
            return None
        
        data = response.json()
        
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S")
        return {
        "Tempreature": data["main"]["temp"], 
        "Feels like": data["main"]["feels_like"], 
        "Min Tempreature": data["main"]["temp_min"], 
        "Max Tempreature": data["main"]["temp_max"], 
        "Pressure": data["main"]["pressure"],
        "Humidity": data["main"]["humidity"],
        "Sunrise": sunrise,
        "Sunset": sunset
        }
    except Exception as e:
        st.error(f"Error occured: {e}")
        return None

    
 
#======== Session Management ========
# Its a session management for logged in user
if 'logged_in' not in st.session_state:
     st.session_state.logged_in = False   


#======== Login Page==================================
def show_login_page():
    """
    It shows login page after running app and verifies login

    args: None
    return: None
    """

    st.title("Login Page Weather App")
    if not st.session_state.logged_in:
            st.subheader("Login Form ")
            username = st.text_input("Enter username")
            password = st.text_input("Enter password", type="password")
            if st.button("Login"):
                if user_login(username, password) and username != password:
                    st.session_state.logged_in = True
                    st.success("Login successful!!!!")
                    st.rerun()
                else:
                    st.error("Invalid username and password possibility of same username and password")   

#============ Weather app ==========   
def show_weather_page():
    """
    After successfull login this page is used to show the weather details.

    Reutrn: weather after giving input city name. Weather details: 
    Tempreature, 
    Feels like, 
    Min Tempreature, 
    Max Tempreature, 
    Pressure,
    Humidity,
    Sunrise,
    Sunset
    """
    st.header("Weather App")
    city = st.text_input("Enter city name:  ")
    if st.button("Get weather"):
        if not city.strip():
            st.warning("Please enter a city name")
        else:
            data = get_weather_city(city)
            if data:
                #st.json(data)
                st.subheader(f"Weather in {city.title()}")
                col1, col2, col3 = st.columns(3)
                col1.metric("🌡️ Tempreature: (°C) ", data["Tempreature"])
                col2.metric("😇 Feels like: (°C)", data["Feels like"])
                col3.metric("💧 Humidity: (%)", data["Humidity"])

                col4, col5, col6 = st.columns(3)
                col4.metric("⬇️ Min Temp (°C): ", data["Min Tempreature"])
                col5.metric("⬆️ Max Temp: (°C)", data["Max Tempreature"])
                col6.metric("🔽 Pressure: ", data["Pressure"])

                col7, col8 = st.columns(2)
                col7.metric("🌅 Sunrise: ", data["Sunrise"])
                col8.metric("🌇 Sunset: ", data["Sunset"])

    
    if st.button("Logout"):
         st.session_state.logged_in =False
         st.rerun()
   
# ===== Page Routing =====
#It is a page routing for an app to navigate from login to app page
if st.session_state.logged_in:
    show_weather_page()
else:
    show_login_page()