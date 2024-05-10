import json
import os

import requests
from dotenv import find_dotenv, load_dotenv

# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio


def get_row_chat_history(
        log_segment_subject: str) -> tuple[tuple[str, str], str]:
    _ = load_dotenv(find_dotenv())
    list_chat_history_api_url: str = os.environ['LIST_CHAT_HISTORY_API_URL']
    url = f"{list_chat_history_api_url}/messages?segment_id={log_segment_subject}"

    headers = {}
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)

    messages = data["messages"]

    row_chat_history = []

    for message in messages:
        if message["user_type"] == "Client":
            row_chat_history.append((None, message["content"]))
        elif message["user_type"] == "TAM":
            row_chat_history.append((message["content"], None))

    prev_summerized_ticket_content = "![](https://img.pikbest.com/png-images/20190918/cartoon-snail-loading-loading-gif-animation_2734139.png!f305cw)"

    return row_chat_history, prev_summerized_ticket_content

def process_tickets(tickets):
    processed_tickets = []
    for ticket in tickets:
        role = ticket.get("Role")
        description = ticket.get("Description")
        if role == "Client":
            processed_tickets.append((None, description))
        elif role == "TAM":
            processed_tickets.append((description, None))
    return processed_tickets
