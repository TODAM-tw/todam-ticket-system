from typing import Any

import gradio as gr

def build_playground(
    *args: Any, **kwargs: Any,) -> gr.Blocks:

    demo = gr.Blocks(
        title='ToDAM Ticket System',
    )

    with demo:
        header = gr.HTML(
            "<h1 align=center>ToDAM Ticket System</h1>"
        )

    return demo
