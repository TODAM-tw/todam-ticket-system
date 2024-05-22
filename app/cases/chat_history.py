import json
import os

import requests

from app.utils.data_type import extract_chat_history
from app.utils.update import render_segment_id

# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio


def get_row_chat_history(
        log_segment_name: str, id_name_comparison: str) -> tuple[tuple[str, str], str]:
    """
    Get the chat history of the segment

    Args:
        - log_segment_name: the name of the segment
        - id_name_comparison: the comparison of the segment name and id

    Returns:
        - row_chat_history: the chat history of the segment
        - message_types: the types of the messages
    """

    log_segment_id           : str = render_segment_id(log_segment_name, id_name_comparison)
    list_chat_history_api_url: str = os.environ.get('LIST_CHAT_HISTORY_API_URL')

    url = f"{list_chat_history_api_url}/messages?segment_id={log_segment_id}"
    headers = {}
    payload = {}
    data = {}

    response = requests.request(
        "GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)

    segment_contents: list[dict] = data["messages"]
    row_chat_history, message_types = extract_chat_history(segment_contents)

    return row_chat_history, message_types
