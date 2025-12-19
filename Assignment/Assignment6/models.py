import streamlit as st
import requests
import os
from dotenv import load_dotenv
import json

# ========================== PAGE CONFIG =======================
st.set_page_config(page_title="Multi-LLM Chatbot", page_icon="🤖", layout="wide")

# ========================== API CONFIG =======================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ========================== SESSION STATE =======================
if "chat" not in st.session_state:
    st.session_state.chat = {
        "GROQ Cloud": [],
        "LM Studio(Local)": []
        }

# ========================== SIDEBAR =======================
with st.sidebar:
    st.sidebar.title("⚙️ Settings")
    model_choice = st.sidebar.radio(
        "Select Model",
        ["GROQ Cloud", "LM Studio(Local)"]
    )

    if st.button("🗑️ Clear Current Chat"):
        st.session_state.chat[model_choice] = []
        st.rerun()

    st.caption(
        f"💬 Messages: {len(st.session_state.chat[model_choice])}"
    )
# ========================== ACTIVE CHAT =======================
active_chat = st.session_state.chat[model_choice]
# ========================== MAIN UI =======================

st.title("🤖 Multi-LLM ChatBot",text_alignment="center")
user_input = st.chat_input("Ask anything ...")

# ========================== FUNCTIONS =======================
def ask_groq(message):
    URL = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    req_data = {
        "model" :"llama-3.3-70b-versatile",
        "messages" : message
    }
    response = requests.post(URL, data=json.dumps(req_data), headers= headers)
    resp = response.json()
    # return st.write(resp)
    return resp["choices"][0]["message"]["content"]
def ask_lm_studio_model(message):
    url = "http://192.168.1.115:1234/v1/chat/completions"
    api_key = "dummy-key"
    headers = {
        "Authorization" : f"Bearer {api_key}",
        "Content-Type" : "application/json"
    }
    req_data = {
        "model" :"llama-3.3-70b-versatile",
        "messages" :message
    }
    response = requests.post(url, data=json.dumps(req_data), headers= headers)
    resp = response.json()
    # return st.write(resp)
    return resp["choices"][0]["message"]["content"]

# ========================== CHAT FLOW  =======================
if user_input:
    # Add user message
    active_chat.append(
        {
            "role" : "user",
            "content": user_input
        }
    )
    # Get response

    if model_choice == "GROQ Cloud":
        answer = ask_groq(active_chat)
    else:
        answer = ask_lm_studio_model(active_chat)

    # Add assistant message 
    active_chat.append({
        "role": "assistant",
        "content": answer
    })
# ========================== DISPLAY CHAT =====================
for msg in st.session_state.chat[model_choice]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])