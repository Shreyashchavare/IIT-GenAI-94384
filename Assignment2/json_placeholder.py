import requests
import json
"""
Fetch data from JSONPlaceholder API and save to a file
"""
url = "https://jsonplaceholder.typicode.com/todos/1"

response = requests.get(url)
print(f"status code: {response.status_code}")

data = response.json()

print("resp data:", data)

with open("response_data.json", "w") as f:
    json.dump(data, f, indent=4)

print("Saved to response_data.json")

