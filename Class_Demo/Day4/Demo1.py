import os
import requests
import json
import time

api_key = os.getenv("GROQ_API_KEY")
URL = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

while True:
    user_prompt = input("Ask something....")
    if user_prompt == "exit":
        break

    req_data = {
        "model" :"llama-3.3-70b-versatile",
        "messages" : [
            {"role" : "user", "content": user_prompt}
        ],
    }

    time1 = time.perf_counter()
    response = requests.post(URL, data=json.dumps(req_data), headers= headers)
    time2 = time.perf_counter()

    print("Status:", response.status_code)
    resp = response.json()
    print(resp["choices"][0]["message"]["content"])
    print(f"Time required: {time2 - time1:.2f} sec")