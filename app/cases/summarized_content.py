import json
import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


def get_summarized_ticket_content(
        log_segment: gr.Dropdown, row_chat_history: gr.Chatbot, message_types) -> tuple[str, str]:
    _ = load_dotenv(find_dotenv())
    bedrock_api_url: str = os.environ['BEDROCK_API_URL']

    message_types_list = convert_message_types_to_list(message_types)

    result = []
    current_user_type = None

    for i in range(len(row_chat_history)):
        tam_message, client_message = row_chat_history[i]
        message_type = message_types_list[i]
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
            "message_type": message_type, # "text" or "image
            "user_type": current_user_type,
            "content": content
        })

    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({"input": result})     # 要再包一層 input

    response: Response = requests.request(
        "POST", bedrock_api_url, 
        headers=headers,
        data=payload
    )

    data = []

    if response.status_code == 200:
        data: dict = json.loads(response.text)
    else:
        return "Error: Something went wrong with the API"

    body = json.loads(data["body"])
    body = body[0]
    content = body["content"]   # list
    content = content[0]

    content_text = content["text"]  # str

    content_text_dict: dict = json.loads(content_text)   # dict
    
    subject: str = content_text_dict["subject"]
    content_transcripts: list = content_text_dict["transcript"]    # list

    case_id = log_segment

    transcript_output = ""

    for i in range(len(content_transcripts)):
        transcript_output += f"<blockquote><h3>Submitted by {content_transcripts[i]['submittedBy']}</h3>Content: {content_transcripts[i]['content']}</blockquote>\n"


    subject_output = f"<h1>Subject: {subject}</h1>"
    summerized_ticket_content = f"<div>\n<h3>Case ID: {case_id}</h3>\n{transcript_output}\n</div>"
    
    return subject_output, summerized_ticket_content


def convert_message_types_to_list(
        message_types: str) -> list:
    # Remove surrounding brackets and any extra whitespace
    cleaned_message_types = message_types.strip("[]").strip()

    # Split the string into a list using comma and space as delimiters
    message_types_list = cleaned_message_types.split(", ")

    # Remove quotes around each element in the list
    message_types_list = [message_type.strip("'") for message_type in message_types_list]

    return message_types_list
