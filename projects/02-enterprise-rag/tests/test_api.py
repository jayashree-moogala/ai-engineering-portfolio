import requests

url = "http://127.0.0.1:8000/ask"

payload = {
    "question": "How many vacation days do employees get?"
}

response = requests.post(url, json=payload)

print(response.json())