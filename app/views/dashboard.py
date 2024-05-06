from typing import Any

import gradio as gr

from app.api.mock import render_logs_summerized_tickets
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
                with gr.Row():
                    summerized_Subject = gr.Markdown(
                        value="# Summerized Subject",
                        line_breaks=True,
                    )
                    Date = gr.Markdown(
                        value="📅 Date",
                        line_breaks=True,
                    )
                with gr.Row():
                    summerized_ticket_conent = gr.Textbox(
                        interactive=True,
                        label="📝 Summerized Ticket Content (shift + enter)",
                        render=True,
                        value=get_text(),
                    )
                    prev_summerized_ticket_content = gr.Markdown(
                        value=get_text(),
                        line_breaks=True,
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
            fn=render_logs_summerized_tickets,
            inputs=log_segment,
            outputs=row_chat_history,
        )

    return demo

def render_preview(summerized_ticket_conent: str) -> str:
    prev_summerized_ticket_content = summerized_ticket_conent
    return prev_summerized_ticket_content

def get_text():
    return """\
# ⚠️ Please click on the "🔄 Refresh Log Segments Records" button to get the latest log segment records.
"""
