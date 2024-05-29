import os

import gradio as gr
import requests

from app.utils.update import remove_subject_tag, render_segment_id


def send_summarized_ticket_content(
    ticket_subject: str, summerized_ticket_content: str, 
    log_segment_name: str, id_name_comparison: str,) -> str:
    """
    Send the summarized ticket content to the API

    Args:
        - ticket_subject (str): The subject of the ticket
        - summerized_ticket_content (str): The summarized ticket content
        - log_segment_name (str): The name of the log segment
        - id_name_comparison (str): The id_name_comparison json string

    Returns:
        - submit_status (str): The status of the submission and will be displayed in the UI
    """

    submit_ticket_api_url: str = os.environ.get('SUBMIT_TICKET_API_URL')
    department_id        : str = os.environ.get('DEPARTMENT_ID')
    log_segment_id       : str = render_segment_id(log_segment_name, id_name_comparison)
    ticket_subject       : str = remove_subject_tag(ticket_subject)

    headers: dict = {
    }

    payload: dict = {
        "ticket_subject"    : ticket_subject,
        "ticket_description": summerized_ticket_content,
        "department_id"     : department_id,
        "segment_id"        : log_segment_id
    }

    try:
        response: requests.Response = requests.request(
            method="POST", 
            url=submit_ticket_api_url, 
            headers=headers, 
            json=payload  # change data to json
        )

        if response.status_code == 200: 
            print(response.text)

        gr.Info("""🚦 Submit Status: Success !!!""")
        submit_status = "🚦 Submit Status: Success !!!"
        return submit_status
    except Exception as e:
        raise gr.Error(f"🚦 Submit Status: Failed, the error is {e}")
