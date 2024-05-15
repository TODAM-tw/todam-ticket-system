import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv


def send_summarized_ticket_content(
    ticket_subject: gr.HTML, summerized_ticket_content: gr.Dropdown, 
    log_segment_subject: gr.Markdown) -> str:
    _ = load_dotenv(find_dotenv())
    department_id        : str = os.environ['DEPARTMENT_ID']
    submit_ticket_api_url: str = os.environ['SUBMIT_TICKET_API_URL']

    ticket_subject = remove_subject_tag(ticket_subject)

    payload = {
        "ticket_subject"    : ticket_subject,
        "ticket_description": summerized_ticket_content,
        "department_id"     : department_id,
        "segment_id"        : log_segment_subject
    }

    headers = {
    }

    try:
        response = requests.request(
            "POST", submit_ticket_api_url, headers=headers, json=payload  # change data to json
        )

        if response.status_code == 200: 
            print(response.text)

        submit_status = "🚦 Submit Status: Success"
        return submit_status
    except Exception as e:
        submit_status = f"🚦 Submit Status: Failed, the error is {e}"
        return submit_status


def remove_subject_tag(subject):
    return subject.replace("<h1>Subject: ", "").replace("</h1>", "")
