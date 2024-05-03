import json

import requests

url = "https://9w7elxl4e9.execute-api.us-east-1.amazonaws.com/Stage/segments"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(type(response.text))

data = json.loads(response.text)

segment_ids = [segment["segment_id"] for segment in data["segments"]]
segment_names = [segment["segment_name"] for segment in data["segments"]]
group_ids = [segment["group_id"] for segment in data["segments"]]

print(segment_ids)
print(segment_names)
print(group_ids)


url = f"https://wgt7ke1555.execute-api.us-east-1.amazonaws.com/dev/messages?segment_id={segment_ids[0]}"
response = requests.request("GET", url, headers=headers, data=payload)
data = json.loads(response.text)
print(data)

messages = data["messages"]

chat_history = []

# Wrap in data structure
# in
for message in data["messages"]:
    if message["user_type"] == "Client":
        chat_history.append((None, message["content"]))
    elif message["user_type"] == "TAM":
        chat_history.append((message["content"], None))

print(chat_history)

