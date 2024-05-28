import gradio as gr


def get_hidden_info_converted() -> tuple[gr.Markdown, gr.Code]:
    """
    Returns the hidden fields for the comparison.

    Args:
        - None

    Returns:
        - message_type (gr.Markdown): The message type
        - id_name_comparison (gr.Code): The id name comparison
    """
    message_type = gr.Markdown(
        value="🧪 Test Type: Playground",
        visible=False,
    )

    id_name_comparison = gr.Code(
        value="",
        language="json",
        visible=False,
    )

    return message_type, id_name_comparison
