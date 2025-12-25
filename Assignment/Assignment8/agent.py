import json
import os
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.agents.middleware import wrap_model_call
import requests
import pandas as pd

# ===================== MIDDLEWARE =====================
@wrap_model_call
def model_logging(request, handler):
    print("Before model call", '-'*20)
    #print request
    response = handler(request)
    print("After model call", '-'*20)
    # print response 
    response.result[0].content.upper()
    return response

@wrap_model_call
def limit_model_context(request, handler):
    print("*Before model call:", '-'*20)
    #print request
    request.messages = request.messages[-5:]
    response = handler(request)
    print("*Before model call:", '-'*20)
    # print response 
    response.result[0].content.upper()
    return response

# ===================== PAGE CONFIG =====================
conversation = []
# ===================== TOOLS =========================
@tool
def calculator(expression: str):
    "Solves aritmentic expressions using +, -, *, / and prentheses."
    try: 
        result = eval(expression)
        return str(result)
    except:
        return "Error: Cannot solve expression."

@tool
def file_reader(file_path: str)-> str:
    "Read the CSV file from its path using pandas"
    try:
        df = pd.read_csv(file_path)
        return(
            f"CSV loaded successfully.\n"
            f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n"
            f"Columns: {list(df.columns)}"
        )
    except Exception as e:
        return f"Error reading CSV: {str(e)}"
@tool
def current_weather(city: str):
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
    
# @tool
# def knowledge_lookup():
    
#     return
# ===================== INIT MODEL =====================
llm = init_chat_model(
    model="google/gemma-3-4b",
    model_provider="openai",
    base_url= "http://localhost:1234/v1",
    api_key = "not-needed"
)
# ===================== CREATE AGENT ===================
system_prompt = """
You are a helpful AI assistant.

GENERAL RULES:
- Think step by step before answering.
- Use tools only when required.
- Do NOT hallucinate tool outputs.

TOOL USAGE GUIDELINES:

1. calculator
- Use when the user asks for math, arithmetic, or numeric comparison.
- Input must be a valid mathematical expression.
- Return only the final numeric result.

2. file_reader
- Use tool if path is given to the input
- Use when the user asks to read, summarize, or extract data from a file.
- Always verify the file path exists before reading.

3. current_weather
- Use when the user asks about weather, temperature, or climate.
- Always ask for city name if missing.

RESPONSE FORMAT:
- Be concise.
- Explain tool results in plain English.
"""

agent = create_agent(
    model=llm,
    tools=[calculator, file_reader, current_weather],
    system_prompt=system_prompt
)

# =====================  USER INPUT =====================
while True:
    user_input = input("Ask something....(for file give path of it)")
    if user_input == "exit":
        break
    #append conversation
    conversation.append({"role": "user", "content": user_input})
    # invoke agent
    result = agent.invoke({
        "messages": conversation
    })
    # Get last AI msg
    ai_msg = result["messages"][-1].content 
    
    # append AI response 
    conversation.append({"role" : "assistant", "content": ai_msg})

# ===================== Display Chat =====================
    for msg in conversation:
        if msg["role"] == "user":
            print("You: ", msg["content"])
        else:
            print("AI : ", msg["content"])

