import json
import os
from typing import Any

import gradio as gr
import requests
from dotenv import find_dotenv, load_dotenv
from requests.models import Response

from app.cases.chat_history import render_row_chat_history
from app.cases.segment import get_segments, get_summerized_ticket_content


def build_playground(
    *args: Any, **kwargs: Any,) -> gr.Blocks:

    with gr.Blocks(
        title='ToDAM Ticket System',
    ) as demo:
        gr.HTML(
            "<h1 align=center>ToDAM Ticket System</h1>"
        )

        with gr.Row():

            with gr.Column(scale=1):
                log_segment = gr.Dropdown(
                    label="🚘 Log Segment Records",
                    info="Select a Record Segment to summerize with 👇🏻",
                    interactive=True,
                    multiselect=None,
                )
                refresh_btn = gr.Button(
                    variant="secondary",
                    value="🔄 Refresh Log Segments Records",
                )

                row_chat_history = gr.Chatbot(
                    label="Chat History Row Data",
                    show_label=True,
                )
            with gr.Column(scale=2):
                # TODO: sync with the chat history
                # with gr.Row():
                #     summerized_Subject = gr.Markdown(
                #         value="# Summerized Subject",
                #         line_breaks=True,
                #     )
                #     date = gr.Markdown(
                #         value="📅 Date",
                #         line_breaks=True,
                #     )
                with gr.Row():
                    summerized_ticket_conent = gr.Textbox(
                        interactive=True,
                        label="📝 Summerized Ticket Content (shift + enter)",
                        render=True,
                        value="""# ⚠️ Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records.""",
                    )

                    # TODO: Change to HTML
                    prev_summerized_ticket_content = gr.Markdown(
                        value="""# ⚠️ Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records.""",
                        line_breaks=True,
                    )

                with gr.Row():
                    regenerate_summerized_ticket_content_btn = gr.Button(
                        variant="secondary",
                        value="🔄 re-generate",
                    )
                    submit_summerized_btn = gr.Button(
                        variant="primary",
                        value="🕹️ Submit to Ticket System",
                    )

        submit_status = gr.Markdown(
            value="🚦 Submit Status: Pending",
            line_breaks=True,
        )

            

        with gr.Row():
            token_cost = gr.Markdown(
                "🔒 Token Cost $: 0.01 USD"
            )

            time_cost = gr.Markdown(
                "⏰ Time Cost: 40 (sec)"
            )
            step_cost = gr.Markdown(
                "🦶🏻 Steps Cost: 5 steps"
            )

        refresh_btn.click(
            fn=get_segments,
            inputs=[log_segment],
            outputs=[log_segment],
        )

        summerized_ticket_conent.change(
            fn=render_preview,
            inputs=summerized_ticket_conent,
            outputs=prev_summerized_ticket_content,
        )

        row_chat_history.change(
            fn=get_summerized_ticket_content,
            inputs=row_chat_history,
            outputs=summerized_ticket_conent,
        )


        log_segment.change(
            fn=render_row_chat_history,
            inputs=log_segment,
            outputs=[row_chat_history, prev_summerized_ticket_content],
        )

        regenerate_summerized_ticket_content_btn.click(
            fn=regenerate_summerized_ticket_content,
            inputs=row_chat_history,
            outputs=summerized_ticket_conent,
        )

        submit_summerized_btn.click(
            fn=submit_summerized_ticket_content,
            inputs=summerized_ticket_conent,
            outputs=submit_status,
        )

    return demo

def render_preview(summerized_ticket_conent: str) -> str:
    prev_summerized_ticket_content = summerized_ticket_conent
    return prev_summerized_ticket_content

def regenerate_summerized_ticket_content(
    row_chat_history: gr.Chatbot) -> str:

    _ = load_dotenv(find_dotenv())
    azure_ml_deployed_url = os.environ['AZURE_ML_DEPLOYED_URL']
    azure_ml_token = os.environ['AZURE_ML_TOKEN']
    azure_model_deployment = os.environ['AZURE_MODEL_DEPLOYMENT']

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
        'azureml-model-deployment': azure_model_deployment,
        'authorization': f"Bearer {azure_ml_token}"
    }

    response: Response = requests.request("POST", azure_ml_deployed_url, headers=headers, data=payload)

    if response.status_code == 200:

        data: dict = json.loads(response.text)

        result: str = json.loads(data["result"])    # result 是一個字串，裡面是一個 JSON 格式的字串
        transcript = result["transcript"]
        case_id = result["caseId"]
        subject = result["subject"]

        transcript_output = ""

        # TODO: Change to HTML
        for item in result['transcript']:
            transcript_output += f"```\nSubmitted by {item['Submitted by']}\nContent: {item['content']}\n```\n\n"

        summerized_ticket_content = f"""\n# Subject: {subject}\n> Case ID: {case_id}\n{transcript_output}"""
        
        return summerized_ticket_content

def submit_summerized_ticket_content(
    summerized_ticket_conent: str) -> str:

    submit_status = "🚦 Submit Status: Success"
    return submit_status

