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


def clean_recording_markers(messages: list[dict]) -> list[dict]:
    """
    Removes 'start recording' marker from the beginning and 
    'end recording' marker from the end of the messages list if they exist.

    Args:
        - messages (list of dict): The list of message dictionaries to clean.

    Returns:
        - message (list of dict): The cleaned list of messages.
    """
    FIRST_INDEX = 0
    LAST_INDEX = -1

    if messages and messages[FIRST_INDEX].get("content") == 'start recording':
        messages.pop(FIRST_INDEX)

    if messages and messages[LAST_INDEX].get("content") == 'end recording':
        messages.pop(LAST_INDEX)

    return messages
