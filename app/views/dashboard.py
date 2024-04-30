from typing import Any

import gradio as gr


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
                log_records = gr.Dropdown(
                    label="🚘 Log Records",
                    info="Select a Record Segment to summerize with 👇🏻",
                    choices=get_choices(),
                    interactive=True,
                    multiselect=None,
                )

                row_chat_history = gr.Chatbot(
                    label="Chat History Row Data",
                    show_label=True,
                )
            with gr.Column(scale=2):
                with gr.Row():
                    summerized_ticket_conent = gr.Textbox(
                        interactive=True,
                        label="📝 Summerized Ticket Content",
                        render=True,
                        value=get_text(),
                    )
                    prev_summerized_ticket_content = gr.Markdown(
                        value=get_text(),
                    )

                retry_btn = gr.Button(
                    variant="secondary",
                    value="🔄 re-generate",
                )
                submit_ticket = gr.Button(
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

        summerized_ticket_conent.change(
            fn=render_preview,
            inputs=summerized_ticket_conent,
            outputs=prev_summerized_ticket_content,
        )

        log_records.change(
            fn=render_logs_summerized_tickets,
            inputs=log_records,
            outputs=[row_chat_history, summerized_ticket_conent],
        )

    return demo

def render_logs_summerized_tickets(log_records):
    if log_records == "v0.0.1":
        row_chat_history = (("Hi", "Hello"), ("How are you?", "I am fine, thank you!"))
        summerized_ticket_conent = "This is a summerized ticket content."
    elif log_records == "v0.0.2":
        row_chat_history = (("Hi2", "Hello2"), ("How are you?2", "I am fine, thank you!2"))
        summerized_ticket_conent = "This is a summerized ticket content.2"
    elif log_records == "v0.0.3":
        row_chat_history = (("Hi3", "Hello3"), ("How are you?3", "I am fine, thank you!3"))
        summerized_ticket_conent = "This is a summerized ticket content.3"

    return row_chat_history, summerized_ticket_conent
    


def render_preview(summerized_ticket_conent: str):
    return summerized_ticket_conent

def get_choices():
    return ["v0.0.1", "v0.0.2", "v0.0.3"]    

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
