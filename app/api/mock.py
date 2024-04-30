import gradio as gr
import requests
from requests.models import Response

# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio

def get_log_segment(log_segment):

    segments = {
        "segments": [
            {
                "segment_id": "segment_id_0001",
                "segment_name": "segment_0001",
                "group_id": "group_id_0001"
            },
            {
                "segment_id": "segment_id_0002",
                "segment_name": "segment_0002",
                "group_id": "grooup_id_0002"
            },
            {
                "segment_id": "segment_id_0003",
                "segment_name": "segment_0003",
                "group_id": "group_id_0001"
            },
            {
                "segment_id": "segment_id_0004",
                "segment_name": "segment_0004",
                "group_id": "grooup_id_0002"
            }
        ]
    }

    # response: Response = requests.get(f"http://0.0.0.0:8080/mock_ticket?id=1")

    response = segments

    segment_names = [segment["segment_name"] for segment in response["segments"]]
    segment_ids = [segment["segment_id"] for segment in response["segments"]]

    print(segment_names)

    log_segment = gr.Dropdown(
        label="🚘 Log Segment Records",
        info="Select a Record Segment to summerize with 👇🏻",
        value=segment_ids[0],
        choices=segment_ids,
        interactive=True,
        multiselect=None,
    )

    row_chat_history = (("Hi", "Hello"), ("How are you?", "I am fine, thank you!"), ("HiHI", None), ("HelloHello", None))

    summerized_ticket_conent = "This is a summerized ticket content."

    return log_segment, row_chat_history, summerized_ticket_conent
    

def render_logs_summerized_tickets(
        log_segment_subject: str) -> tuple[tuple[str, str], str]:
    if log_segment_subject == "segment_id_0001":
        row_chat_history = (("Hi", "Hello"), ("How are you?", "I am fine, thank you!"), ("HiHI", None), ("HelloHello", None))
        summerized_ticket_conent = "This is a summerized ticket content."
    elif log_segment_subject == "segment_id_0002":
        row_chat_history = (("Hi2", "Hello2"), ("How are you?2", "I am fine, thank you!2"))
        summerized_ticket_conent = "This is a summerized ticket content.2"
    elif log_segment_subject == "segment_id_0003":
        row_chat_history = (("Hi3", "Hello3"), ("How are you?3", "I am fine, thank you!3"))
        summerized_ticket_conent = "This is a summerized ticket content.3"

    return row_chat_history, summerized_ticket_conent


if __name__ == "__main__":
    get_log_segment()
