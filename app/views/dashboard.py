import json
from typing import Any

import gradio as gr

from app.cases.chat_history import get_row_chat_history
from app.cases.segment import get_segments
from app.cases.submit import send_summarized_ticket_content
from app.cases.summarized_content import get_summarized_ticket_content


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
                log_segment_name = gr.Dropdown(
                    label="🚘 Log Segment Records (Name)",
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
                #     summarized_Subject = gr.Markdown(
                #         value="# Summarized Subject",
                #         line_breaks=True,
                #     )
                #     date = gr.Markdown(
                #         value="📅 Date",
                #         line_breaks=True,
                #     )
                with gr.Row():
                    summarized_ticket_conent = gr.Textbox(
                        interactive=True,
                        label="📝 Summarized Ticket Content (shift + enter)",
                        render=True,
                        value="""<h1> ⚠️ Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records. </h1>""",
                    )

                    with gr.Row():
                        with gr.Column():
                            prev_summarized_ticket_subject = gr.HTML(
                                value="""Subject: """,
                            )
                        with gr.Column():
                            prev_summarized_ticket_content = gr.HTML(
                                # value="""Content""",
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

        submit_status = gr.Markdown(
            value="🚦 Submit Status: Pending",
            line_breaks=True,
        )

        message_type = gr.Markdown(
            value="🧪 Test Type: Playground",
        )   

        id_name_comparison = gr.Code(
            value="",
            language="json",
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
            inputs=[log_segment_name],
            outputs=[log_segment_name, id_name_comparison],
        )
        


        log_segment_name.change(
            fn=get_row_chat_history,
            inputs=[log_segment_name, id_name_comparison],
            outputs=[row_chat_history, message_type],
        )

        summarized_ticket_conent.change(
            fn=render_preview,
            inputs=summarized_ticket_conent,
            outputs=prev_summarized_ticket_content,
        )

        row_chat_history.change(
            fn=get_summarized_ticket_content,
            inputs=[log_segment_name, id_name_comparison, row_chat_history, message_type],
            outputs=[prev_summarized_ticket_subject, summarized_ticket_conent],
        )

        regenerate_summarized_ticket_content_btn.click(
            fn=get_summarized_ticket_content,
            inputs=[log_segment_name, id_name_comparison, row_chat_history, message_type],
            outputs=[prev_summarized_ticket_subject, summarized_ticket_conent],
        )

        submit_summarized_btn.click(
            fn=send_summarized_ticket_content,
            inputs=[prev_summarized_ticket_subject, summarized_ticket_conent, log_segment_name, id_name_comparison,],
            outputs=submit_status,
        )

    return demo

def render_preview(summarized_ticket_conent: str) -> str:
    prev_summarized_ticket_content = summarized_ticket_conent
    return prev_summarized_ticket_content
