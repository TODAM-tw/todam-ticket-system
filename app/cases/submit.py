import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv


def send_summerized_ticket_content(
    summerized_ticket_content: gr.Dropdown, log_segment_subject: gr.Markdown) -> str:
    _ = load_dotenv(find_dotenv())
    department_id: str = os.environ['DEPARTMENT_ID']
    submit_ticket_api_url = os.environ['SUBMIT_TICKET_API_URL']

    payload = {
        "ticket_subject"    : "test by Hugo",   # TODO: subject 之後要獨立出 get_summerized_ticket_content()
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
        print(e)
        submit_status = "🚦 Submit Status: Failed"
        return submit_status
