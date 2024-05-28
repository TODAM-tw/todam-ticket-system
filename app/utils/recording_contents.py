def extract_chat_history(
        segment_contents: list[dict]) -> tuple[list[tuple[str, str]], str]:
    """
    Extract chat history from the content of segment

    Args:
        - segment_contents (list of dict): The list of segment contents

    Returns:
        - chat_history (list of tuple(str, str): the chat history of the segment
        - message_types (str): the types of the messages
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
    START_RECORDING_INDEX = 0
    END_RECORDING_INDEX = -1

    if messages and messages[START_RECORDING_INDEX].get("content") == 'start recording':
        messages.pop(START_RECORDING_INDEX)

    if messages and messages[END_RECORDING_INDEX].get("content") == 'end recording':
        messages.pop(END_RECORDING_INDEX)

    return messages


def convert_message_types_to_list(
        message_types: str) -> list:
    """
    Convert the message types string to a list of message types

    Args:
        - message_types (str): The message types string

    Returns:
        - message_types_list (list): The list of message types
    """
    cleaned_message_types = message_types.strip("[]").strip()
    
    message_types_list = cleaned_message_types.split(", ")
    message_types_list = [message_type.strip("'") for message_type in message_types_list]

    return message_types_list
