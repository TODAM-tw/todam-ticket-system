from typing import Any

import gradio as gr

from app.cases.chat_history import get_row_chat_history
from app.cases.segment import get_segments
from app.cases.submit import send_summerized_ticket_content
from app.cases.summerized_content import get_summerized_ticket_content


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
                # Need to be researched to get the latest log segments
                # log_segment_name = gr.Dropdown(
                #     label="🚘 Log Segment Records (Name)",
                #     info="Select a Record Segment to summerize with 👇🏻",
                #     interactive=True,
                #     multiselect=None,
                # )
                log_segment_id = gr.Dropdown(
                    label="🚘 Log Segment Records (ID)",
                    info="Select a Record Segment to summerize with 👇🏻",
                    interactive=True,
                    multiselect=None,
                    # visible=False,
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
            inputs=[log_segment_id],
            outputs=[log_segment_id],
        )
        

        # log_segment_name.change(
        #     fn=get_row_chat_history,
        #     inputs=log_segment_id,
        #     outputs=[log_segment_id, row_chat_history, prev_summerized_ticket_content],
        # )

        log_segment_id.change(
            fn=get_row_chat_history,
            inputs=log_segment_id,
            outputs=[row_chat_history, prev_summerized_ticket_content],
        )

        row_chat_history.change(
            fn=get_summerized_ticket_content,
            inputs=row_chat_history,
            outputs=summerized_ticket_conent,
        )

        summerized_ticket_conent.change(
            fn=render_preview,
            inputs=summerized_ticket_conent,
            outputs=prev_summerized_ticket_content,
        )

        regenerate_summerized_ticket_content_btn.click(
            fn=get_summerized_ticket_content,
            inputs=row_chat_history,
            outputs=summerized_ticket_conent,
        )

        submit_summerized_btn.click(
            fn=send_summerized_ticket_content,
            inputs=[summerized_ticket_conent, log_segment_id],
            outputs=submit_status,
        )

    return demo

def render_preview(summerized_ticket_conent: str) -> str:
    prev_summerized_ticket_content = summerized_ticket_conent
    return prev_summerized_ticket_content
