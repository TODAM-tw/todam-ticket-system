import json
import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv


def get_segments(
        log_segment: gr.Dropdown) -> gr.Dropdown:
    """
    Get segments from the API

    Args:
        log_segment (gr.Dropdown): Dropdown object

    Returns:
        gr.Dropdown: Dropdown object
    """
    _ = load_dotenv(find_dotenv())
    list_log_segment_api_url: str = os.environ['LIST_LOG_SEGMENT_API_URL']

    payload = {}
    headers = {}

    response = requests.request(
        method="GET", url=list_log_segment_api_url, headers=headers, data=payload
    )
    if response.status_code == 200:
        data = json.loads(response.text)

    segment_ids = [segment["segment_id"] for segment in data["segments"]]
    segment_names = [segment["segment_name"] for segment in data["segments"]]
    group_ids = [segment["group_id"] for segment in data["segments"]]

    log_segment = gr.Dropdown(
        label="🚘 Log Segment Records",
        info="Select a Record Segment to summerize with 👇🏻",
        value=segment_ids[0],
        choices=segment_ids,
        interactive=True,
        multiselect=None,
    )

    return log_segment
