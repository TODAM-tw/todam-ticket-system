from typing import Any

import gradio as gr

from app.utils.listener import background_listener
from app.views.components.converted import get_hidden_info_converted
from app.views.components.information import title
from app.views.components.status_bar import get_status_bar


def build_playground(
    *args: Any, **kwargs: Any,) -> gr.Blocks:
    """
    Build the playground with gradio components.

    Args:
        - *args (Any): The args
        - **kwargs (Any): The kwargs
    
    Returns:
        - demo (gr.Blocks): The gradio blocks
    """

    with gr.Blocks(title=f"{title}") as demo:

        gr.HTML(f"<h1 align=center>{title}</h1>")

        with gr.Row():

            with gr.Column(scale=1):
                log_segment_name = gr.Dropdown(
                    label="🚘 Log Segment Records (Name)",
                    info="Select a Recorded Segment to summerize with 👇🏻",
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
                    summarized_ticket_conent = gr.Textbox(
                        interactive=True,
                        label="📝 Summarized Ticket Content (shift + enter)",
                        render=True,
                        value="""<blockquote>⚠️ Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records.</blockquote>""",
                    )

                    with gr.Row():
                        with gr.Column():
                            preview_summarized_ticket_subject = gr.HTML(
                                value="""<h1>Subject: </h1>""",
                            )
                        with gr.Column():
                            preview_summarized_ticket_content = gr.HTML(
                                value="""<blockquote>⚠️ Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records.</blockquote>""",
                            )

                with gr.Row():
                    regenerate_summarized_ticket_content_btn = gr.Button(
                        variant="secondary",
                        value="🔄 re-generate",
                    )
                    submit_summarized_btn = gr.Button(
                        variant="primary",
                        value="🕹️ Submit to Ticket System",
                    )

        message_type, id_name_comparison = get_hidden_info_converted()

        with gr.Row():
            token_cost, token_usage, submit_status = get_status_bar()

        background_listener(
            refresh_btn, log_segment_name, 
            id_name_comparison, row_chat_history, 
            message_type, summarized_ticket_conent, 
            preview_summarized_ticket_subject, 
            preview_summarized_ticket_content, 
            token_usage, token_cost, 
            regenerate_summarized_ticket_content_btn, 
            submit_summarized_btn, submit_status
        )

    return demo
