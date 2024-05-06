import gradio as gr
import requests
from requests.models import Response
import json

# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio


def render_logs_summerized_tickets(
        log_segment_subject: str) -> tuple[tuple[str, str], str]:
    url = f"https://wgt7ke1555.execute-api.us-east-1.amazonaws.com/dev/messages?segment_id={log_segment_subject}"

    headers = {}
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    messages = data["messages"]

    row_chat_history = []

    for message in messages:
        if message["user_type"] == "Client":
            row_chat_history.append((None, message["content"]))
        elif message["user_type"] == "TAM":
            row_chat_history.append((message["content"], None))

    print(row_chat_history)

    return row_chat_history

def summerized_by_model(row_chat_history_segment):
    return f"""\
{row_chat_history_segment}
"""

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

