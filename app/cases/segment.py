import json
import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv


def get_segments(
        log_segment: gr.Dropdown) -> tuple[gr.Dropdown, str]:
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


    segment_id_name_map = {segment["segment_id"]: segment["segment_name"] for segment in data["segments"]}

    segment_id_name_map_str = json.dumps(segment_id_name_map, ensure_ascii=False, indent=4)

    log_segment = gr.Dropdown(
        label="🚘 Log Segment Records (ID)",
        info="Select a Record Segment to summerize with 👇🏻",
        value=segment_ids[0],
        choices=segment_ids,
        interactive=True,
        multiselect=None,
    )

    return log_segment, segment_id_name_map_str



# TODO: 
# Need to be researched to wrap the following code into a class
# and we can get the comparison between segment id and segment name.
class LogSegment:
    """
    LogSegment class
    """
    def __init__(self,):
        pass

    def update_segment_id(self, segment_id: str) -> str:
        """
        Update segment id

        Args:
            segment_id (str): segment id

        Returns:
            str: segment id
        """
        self.segment_id = segment_id
        return self.segment_id


if __name__ == "__main__":
    log_segment = gr.Dropdown(
        label="🚘 Log Segment Records",
        info="Select a Record Segment to summerize with 👇🏻",
    )
    log_segment, log_segment_name = get_segments(log_segment)
    print(log_segment)
    print(log_segment_name)

    log_segment = LogSegment()
    log_segment, log_segment_name = log_segment.get_segments(log_segment)
