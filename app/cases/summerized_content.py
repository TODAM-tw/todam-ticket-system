import json
import os

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv
from requests.models import Response


def get_summerized_ticket_content(
        row_chat_history: gr.Chatbot) -> str:
    _ = load_dotenv(find_dotenv())
    azure_ml_deployed_url : str = os.environ['AZURE_ML_DEPLOYED_URL']
    azure_ml_token        : str = os.environ['AZURE_ML_TOKEN']
    azure_model_deployment: str = os.environ['AZURE_MODEL_DEPLOYMENT']

    result = []
    current_user_type = None
    message_type = None

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
    
    # TODO: Add Message Type
    payload = str(result)

    headers = {
        'azureml-model-deployment': azure_model_deployment,
        'authorization': f"Bearer {azure_ml_token}"
    }

    response: Response = requests.request(
        "POST", azure_ml_deployed_url, 
        headers=headers, data=payload
    )

    if response.status_code == 200:
        data: dict = json.loads(response.text)
    else:
        return "Error: Something went wrong with the API"

    result: dict = json.loads(data["result"])    # data["result"] 裡面是一個 JSON 格式的字串
    transcript = result["transcript"]
    case_id = result["caseId"]
    subject = result["subject"]

    transcript_output = ""

    # TODO: Change to HTML
    for item in result['transcript']:
        transcript_output += f"> Submitted by {item['Submitted by']}\n> Content: {item['content']}\n\n\n"

    summerized_ticket_content = f"""\n# Subject: {subject}\n- Case ID: {case_id}\n{transcript_output}\n\n\n"""
    
    return summerized_ticket_content