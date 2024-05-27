import json
import os

import gradio as gr
import requests
from requests.models import Response

from app.utils.recording_contents import convert_message_types_to_list
from app.utils.update import render_segment_id


def get_summarized_ticket_content(
        log_segment_name: str, id_name_comparison: str, 
        row_chat_history: gr.Chatbot, message_types: str) -> tuple[str, str]:
    """
    Get the summarized ticket content from the Bedrock API.

    Args:
        - log_segment_name (str): The name of the log segment.
        - id_name_comparison (str): The comparison between the ID and name.
        - row_chat_history (gr.Chatbot): The chat history.
        - message_types (str): The message types.

    Returns:
        - subject_output (str): The subject of the ticket.
        - summerized_ticket_content (str): The summarized ticket content.
    """

    log_segment_id = render_segment_id(log_segment_name, id_name_comparison)
    message_types_list = convert_message_types_to_list(message_types)
    bedrock_api_url: str = os.environ.get('BEDROCK_API_URL')
    
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
            "message_type": message_type,
            "user_type"   : current_user_type,
            "content"     : content
        })

    headers = {
        'Content-Type': 'application/json'
    }

    payload: str = json.dumps({"input": result})     # 要再包一層 input

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

    if type(body) == list:
        body = body[0]
    elif type(body) == dict:
        pass
    else :
        return """Error: the output of data["body"] is not a list or dict"""

    usage: dict[int, int] = body["usage"]
    input_tokens: int = usage["input_tokens"]
    output_tokens: int = usage["output_tokens"]

    content: list = body["content"]
    content = content[0]

    content_text: str = content["text"]

    content_text_dict: dict = json.loads(content_text)
    
    subject: str = content_text_dict["subject"]
    content_transcripts: list = content_text_dict["transcript"]

    transcript_output = ""

    for i in range(len(content_transcripts)):
        transcript_output += f"<blockquote><h3>Submitted by {content_transcripts[i]['submittedBy']}</h3>{content_transcripts[i]['content']}</blockquote>\n"


    subject_output = f"<h1>Subject: {subject}</h1>"
    summerized_ticket_content = f"<div>\n<h3>Case Name: {log_segment_name}</h3>\n{transcript_output}\n</div>"
    
    return subject_output, summerized_ticket_content
