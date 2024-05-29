import json
import os

import gradio as gr
import requests
from requests.models import Response

from app.utils.summarized import (calculate_token_cost, extract_payload_inputs,
                                  format_summarized_transcripts, extract_content_text)


def get_summarized_ticket_content(
        log_segment_name: str, row_chat_history: tuple[str, str], 
        message_types: str) -> tuple[str, str, str, str, str]:
    """
    Get the summarized ticket content from the Bedrock API.
    Also calculate the token usage and cost.

    Args:
        - log_segment_name (str): The name of the log segment.
        - id_name_comparison (str): The comparison between the ID and name.
        - row_chat_history (tuple[str, str]): The chat history.
        - message_types (str): The message types.

    Returns:
        - preview_subject_title (str): The subject of the ticket.
        - preview_summerized_ticket_content (str): The previewiew summarized ticket content.
        - summerized_ticket_content (str): The summarized ticket content.
        - token_usage (str): The token usage.
        - token_cost (str): The token cost.
    """

    gr.Info("""Please wait for the model to finish summarizing before operating on the screen! 🙏🏻""")

    COST_PER_INPUT_TOKEN : float =  3.00 / 1_000_000
    COST_PER_OUTPUT_TOKEN: float = 15.00 / 1_000_000

    bedrock_api_url: str = os.environ.get('BEDROCK_API_URL')

    headers: dict = {
        'Content-Type': 'application/json'
    }

    payload_inputs: list[dict] = extract_payload_inputs(
        row_chat_history, message_types
    )
    payload: str = json.dumps({"input": payload_inputs})     # 要再包一層 input

    response: Response = requests.request(
        method="POST", 
        url=bedrock_api_url, 
        headers=headers,
        data=payload,
    )

    data = []

    if response.status_code == 200:
        data: dict = json.loads(response.text)
    elif response.status_code == 400:
        advice = json.loads(response.text)["advice"]
        raise gr.Error(f"Error: {advice}")
    elif response.status_code == 500:
        advice = json.loads(response.text)["advice"]
        raise gr.Error(f"Error: {advice}")
    else:
        advice = json.loads(response.text)["advice"]
        raise gr.Error(f"Error: {advice}")

    body = json.loads(data["body"])

    if type(body) == list:
        body = body[0]
    elif type(body) == dict:
        pass
    else :
        return """Error: the output of data["body"] is not a list or dict"""

    content_text = extract_content_text(body)

    preview_subject_title, summerized_ticket_content = format_summarized_transcripts(
        log_segment_name, content_text
    )
    token_usage, token_cost = calculate_token_cost(
        body, COST_PER_INPUT_TOKEN, COST_PER_OUTPUT_TOKEN
    )
    preview_summerized_ticket_content = summerized_ticket_content
    
    return (preview_subject_title, preview_summerized_ticket_content, 
            summerized_ticket_content, token_usage, token_cost)
