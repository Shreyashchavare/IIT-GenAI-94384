import os
import requests
import json
import time
import streamlit as st

st.title("My ChatBot")

api_key = "dummy-key"
url = "http://10.67.33.200:1234/v1/chat/completions"
headers = {
    "Authorization" : f"Bearer {api_key}",
    "Content-Type" : "application/json"
}

user_promt = st.chat_input("Ask something....")

if user_promt:
    req_data = {
        "model": "google/gemma-3-4b",
        "messages" :[
            {"role": "user", "content": user_promt}
        ],
    }

    response = requests.post(url, data=json.dumps(req_data), headers= headers)
    resp = response.json()
    st.write(resp["choices"][0]["message"]["content"])