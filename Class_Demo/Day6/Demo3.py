import streamlit as st
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from dotenv import load_dotenv
import os
import json
import requests

# ===================== LOAD ENV =====================
load_dotenv()

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="LangChain Multi-Tool Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 LangChain Multi-Tool Agent (Local LLM)",text_alignment="center")

# ===================== TOOLS =========================
@tool
def calculator(expression: str):
    """
    Solves arithmetic expressions using +, -, *, / and parentheses.
    """
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression"


@tool
def get_weather(city: str):
    """
    Gets current weather of a given city using OpenWeather API.
    """
    try:
        api_key = os.getenv("OPEN_WEATHER_API")
        if not api_key:
            return "Error: API key not found"

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?appid={api_key}&units=metric&q={city}"
        )
        response = requests.get(url)
        weather = response.json()
        return json.dumps(weather)
    except:
        return "Error"


@tool
def read_file(filepath: str):
    """
    Reads a local file and returns its content.
    """
    try:
        with open(filepath, "r") as file:
            return file.read()
    except:
        return "Error: Cannot read file"

# ===================== INIT MODEL =====================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url="http://192.168.1.115:1234/v1",
    api_key="non-needed"
)

# ===================== CREATE AGENT ===================
agent = create_agent(
    model=llm,
    tools=[
        calculator,
        get_weather
        # read_file  # keep commented unless you want file access
    ],
    system_prompt="You are a helpful assistant. Answer in short."
)

# ===================== SESSION STATE ==================
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# ===================== DISPLAY CHAT ===================
for msg in st.session_state.conversation:
    if msg.type == "human":
        st.chat_message("user").write(msg.content)
    elif msg.type == "ai":
        st.chat_message("assistant").write(msg.content)

# ===================== USER INPUT =====================
user_input = st.chat_input(
    "Ask something (math, weather, etc.)"
)

if user_input:
    # Show user message
    st.chat_message("user").write(user_input)

    # Append user message
    st.session_state.conversation.append(
        {"role": "user", "content": user_input}
    )

    # Invoke agent
    result = agent.invoke({
        "messages": st.session_state.conversation
    })

    # Get last AI message
    ai_msg = result["messages"][-1]

    # Show AI response
    st.chat_message("assistant").write(ai_msg.content)

    # Update conversation history
    st.session_state.conversation = result["messages"]
