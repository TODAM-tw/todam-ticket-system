def extract_chat_history(
        segment_contents: list[dict]) -> tuple[list[tuple[str, str]], str]:
    """
    Extract chat history from the content of segment

    Args:
        - segment_contents: the content of the segment

    Returns:
        - chat_history: the chat history of the segment
        - message_types: the types of the messages
    """

    chat_history = []
    message_types_list = []

    for segment_content in segment_contents:
        message_types_list.append(segment_content["message_type"])
        if segment_content["user_type"] == "Client":
            chat_history.append((None, segment_content["content"]))
        elif segment_content["user_type"] == "TAM":
            chat_history.append((segment_content["content"], None))

    return chat_history, str(message_types_list)
