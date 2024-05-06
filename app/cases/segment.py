import json
import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv

GROUP_IDS = None

def get_segments(
        log_segment: gr.Dropdown) -> gr.Dropdown:
    """
    Get segments from the API

    Args:
        log_segment (gr.Dropdown): Dropdown object

    Returns:
        gr.Dropdown: Dropdown object
    """
    url: str = "https://9w7elxl4e9.execute-api.us-east-1.amazonaws.com/Stage/segments"

    payload = {}
    headers = {}

    response = requests.request(
        method="GET", url=url, headers=headers, data=payload
    )

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


def get_segment_row_chat_history(
        log_segment: gr.Dropdown) -> gr.Chatbot:
    """"""
    url = f"https://wgt7ke1555.execute-api.us-east-1.amazonaws.com/dev/messages?segment_id={log_segment}"

    headers = {}
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    data = json.loads(response.text)
    messages = data["messages"]

    chat_history = []

    for message in messages:
        if message["user_type"] == "Client":
            chat_history.append((None, message["content"]))
        elif message["user_type"] == "TAM":
            chat_history.append((message["content"], None))

    return chat_history

def get_summerized_ticket_content(
        row_chat_history: gr.Chatbot) -> str:
    _ = load_dotenv(find_dotenv())
    azure_ml_deployed_url = os.environ['AZURE_ML_DEPLOYED_URL']
    azure_ml_token = os.environ['AZURE_ML_TOKEN']

    result = []
    current_user_type = None

    for item in row_chat_history:
        tam_message, client_message = item
        if tam_message:
            current_user_type = "TAM"
            content = tam_message
        elif client_message:
            current_user_type = "Client"
            content = client_message
        else:
            # Skip recording messages
            continue
        
        result.append({
            "user_type": current_user_type,
            "content": content
        })
    
    payload = str(result)

    headers = {
        'azureml-model-deployment': 'todam-aml-workspace-dev-0503-v1',
        'authorization': f"Bearer {azure_ml_token}"
    }

    response = requests.request("POST", azure_ml_deployed_url, headers=headers, data=payload)


    data: dict = json.loads(response.text)

    result: str = json.loads(data["result"])    # result 是一個字串，裡面是一個 JSON 格式的字串
    transcript = result["transcript"]
    case_id = result["caseId"]
    subject = result["subject"]
    print(subject)

    markdown_output = ""

    for item in result['transcript']:
        markdown_output += f"```\nSubmitted by {item['Submitted by']}\nContent: {item['content']}\n```\n\n"

    summerized_ticket_content = f"""\n# Subject: {subject}\n> Case ID: {case_id}\n{markdown_output}"""

    return summerized_ticket_content
