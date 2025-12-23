from datetime import datetime
from langchain.chat_models import init_chat_model
import os
import streamlit as st
import requests
import json

# ====================== PAGE CONFIG ======================
st.set_page_config(
    page_title="Weather Condition Agent",
    page_icon="⛅",
    layout="wide"
)

st.title(
    "⛅ Weather Condition Agent",
    text_alignment="center"
)

# ====================== LLM CONFIG ======================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://10.67.33.200:1234/v1",
    api_key="dummy-key"
)


# ====================== SESSION CONFIG ===================
if "weather" not in st.session_state:
    st.session_state.weather = []

# ====================== CHAT INPUT ======================
city = st.chat_input("Enter the city name: ")

# Store user message
if city:
    st.session_state.weather.append({
        "role": "user",
        "content": city
    })

    # ====================== WEATHER API ======================
    api_key = os.getenv("OPEN_WEATHER_API")

    if not api_key:
        assistant_reply = " Weather API key not found."
    else:
        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )
        response = requests.get(url)
        result = response.json()
        sunrise = datetime.fromtimestamp(result["sys"]["sunrise"]).strftime("%H:%M:%S")
        sunset = datetime.fromtimestamp(result["sys"]["sunset"]).strftime("%H:%M:%S")
        weather_data ={
        "Tempreature": result["main"]["temp"], 
        "Feels like": result["main"]["feels_like"], 
        "Min Tempreature": result["main"]["temp_min"], 
        "Max Tempreature": result["main"]["temp_max"], 
        "Pressure": result["main"]["pressure"],
        "Humidity": result["main"]["humidity"],
        "Sunrise": sunrise,
        "Sunset": sunset
        }
        
                
        # ====================== LLM PROMPT ======================
        llm_prompt = f"""
        You are a weather analyst.

        Weather data (JSON):
        {json.dumps(weather_data, indent=2)}

        Instructions:
        - Explain the weather in simple English
        - Avoid technical terms
        - Use emojis
        """

        # Invoke LLM
        llm_response = llm.invoke(llm_prompt)
        assistant_reply = llm_response.content
        
        # Store assistant message
        st.session_state.weather.append({
            "role": "assistant",
            "content": assistant_reply
        })

# ====================== DISPLAY CHAT ======================
st.divider()
st.subheader("💬 Conversation")

for msg in st.session_state.weather:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        col1, col2, col3 = st.columns(3)
        col1.metric("🌡️ Tempreature: (°C) ", weather_data["Tempreature"])
        col2.metric("😇 Feels like: (°C)", weather_data["Feels like"])
        col3.metric("💧 Humidity: (%)", weather_data["Humidity"])

        col4, col5, col6 = st.columns(3)
        col4.metric("⬇️ Min Temp (°C): ", weather_data["Min Tempreature"])
        col5.metric("⬆️ Max Temp: (°C)", weather_data["Max Tempreature"])
        col6.metric("🔽 Pressure: ", weather_data["Pressure"])

        col7, col8 = st.columns(2)
        col7.metric("🌅 Sunrise: ", weather_data["Sunrise"])
        col8.metric("🌇 Sunset: ", weather_data["Sunset"])
        st.chat_message("assistant").write(msg["content"])
