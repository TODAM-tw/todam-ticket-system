from typing import Any

import gradio as gr

from app.api.mock import get_log_segment
from app.api.mock import render_logs_summerized_tickets

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
                with gr.Row():
                    summerized_ticket_conent = gr.Textbox(
                        interactive=True,
                        label="📝 Summerized Ticket Content (shift + enter)",
                        render=True,
                        value=get_text(),
                    )
                    prev_summerized_ticket_content = gr.Markdown(
                        value=get_text(),
                    )

                regen_summerized_btn = gr.Button(
                    variant="secondary",
                    value="🔄 re-generate",
                )
                submit_summerized_btn = gr.Button(
                    variant="primary",
                    value="🕹️ Submit to Ticket System",
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
            fn=get_log_segment,
            inputs=[log_segment],
            outputs=[log_segment, row_chat_history, summerized_ticket_conent],
        )

        summerized_ticket_conent.change(
            fn=render_preview,
            inputs=summerized_ticket_conent,
            outputs=prev_summerized_ticket_content,
        )


        log_segment.change(
            fn=render_logs_summerized_tickets,
            inputs=log_segment,
            outputs=[row_chat_history, summerized_ticket_conent],
        )

    return demo




    
def render_preview(summerized_ticket_conent: str) -> str:
    prev_summerized_ticket_content = summerized_ticket_conent
    return prev_summerized_ticket_content

def get_text():
    return """\
# Hi There!
This is a demo of the ToDAM Ticket System.

## How to use?

1. Select a model version to chat with.
2. Type your message in the text box.
3. Click on the "Send" button to send the message.
4. Click on the "Refresh" button to clear the chat history.
5. Click on the "re-generate" button to re-generate the chat history.

## What is the cost?

- Token Cost $: 0.01 USD
- Time Cost: 40 (sec)
- Steps Cost: 5 steps
"""
