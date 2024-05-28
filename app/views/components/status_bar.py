import gradio as gr


def get_status_bar() -> tuple[gr.Markdown, gr.Markdown, gr.Markdown]:
    """
    Returns the status bar.

    Args:
        - None
    Returns:
        - token_cost (gr.Markdown): The token cost
        - token_usage (gr.Markdown): The token usage
        - submit_status (gr.Markdown): The submit status
    """
    token_cost = gr.Markdown(
        "💰 Token Cost:"
    )

    token_usage = gr.Markdown(
        "🔒 Token Usage:"
    )

    submit_status = gr.Markdown(
        value="🚦 Submit Status: Pending",
        line_breaks=True,
    )

    return token_cost, token_usage, submit_status
