import json
import os

import gradio as gr
import requests


# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio

def get_segment_names(
        log_segment_name: gr.Dropdown) -> tuple[gr.Dropdown, gr.Dropdown, str]:
    """
    Get segment names from the API and get the map of segment_id to segment_name

    Args:
        - log_segment_name: The gradio Dropdown object as the trigger to get the segment names

    Returns:
        - log_segment_name: The updated log_segment_name Dropdown object
        - segment_id_name_map_str: The map of segment_id to segment_name in JSON string
    """
    gr.Info("""Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records""")

    list_log_segment_api_url: str = os.environ.get('LIST_LOG_SEGMENT_API_URL')

    headers: dict = {
    }
    payload: dict = {
    }

    response: requests.Response = requests.request(
        method="GET", url=list_log_segment_api_url, 
        headers=headers, data=payload
    )
    if response.status_code == 200:
        data = json.loads(response.text)

    segment_names = [segment["segment_name"] for segment in data["segments"]]
    # TODO: Handle the enrolled group ids to display the group name
    group_ids = [segment["group_id"] for segment in data["segments"]]

    segment_id_name_map = {
        segment["segment_id"]: segment["segment_name"] for segment in data["segments"]
    }
    segment_id_name_map_str = json.dumps(
        segment_id_name_map, ensure_ascii=False, indent=4
    )

    log_segment_name = gr.Dropdown(
        label="🚘 Log Segment Records (Name)",
        info="Select a Record Segment to summerize with 👇🏻",
        value=segment_names[0],
        choices=segment_names,
        interactive=True,
        multiselect=None,
    )

    return log_segment_name, segment_id_name_map_str
