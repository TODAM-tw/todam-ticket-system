import json

from app.utils.recording_contents import convert_message_types_to_list


def extract_payload_inputs(
        row_chat_history: tuple[str, str], message_types: str) -> list[dict]:
    """
    Extracts the payload inputs from the given chat history and message types.
    Also convert the message types to a list.

    Args:
        - row_chat_history (tuple[str, str]): The chat history.
        - message_types (str): The message types.

    Returns:
        - payload_inputs (list[dict]): A list of payload inputs 
        containing message type, user type, and content.
    """

    payload_inputs = []
    current_user_type = None
    message_types_list = convert_message_types_to_list(message_types)

    for i in range(len(row_chat_history)):
        tam_message, client_message = row_chat_history[i]
        message_type = message_types_list[i]
        if tam_message:
            current_user_type = "TAM"
            content = tam_message
        elif client_message:
            current_user_type = "Client"
            content = client_message
        else:
            continue    # Skip recording messages
        payload_inputs.append({
            "message_type": message_type,
            "user_type"   : current_user_type,
            "content"     : content
        })
        
    return payload_inputs


def calculate_token_cost(
        body: dict, COST_PER_INPUT_TOKEN: float = 3.00 / 1_000_000, 
        COST_PER_OUTPUT_TOKEN: float = 15.00 / 1_000_000) -> tuple[str, str]:
    """
    Calculate the total token usage and cost for a given input and output token count.

    Args:
        - body (dict): A dictionary containing usage information.
        - COST_PER_INPUT_TOKEN (float): The cost per input token. Default is `3.00 / 1_000_000` USD.
        - COST_PER_OUTPUT_TOKEN (float): The cost per output token. Default is `15.00 / 1_000_000` USD.

    Returns:
        - token_usage (str): A string describing the token usage.
        - token_cost (str): A string describing the total cost in USD.
    """

    usage: dict[int, int] = body["usage"]
    input_token : int = usage["input_tokens"]
    output_token: int = usage["output_tokens"]

    total_token: int = input_token + output_token
    total_cost: float = input_token * COST_PER_INPUT_TOKEN + output_token * COST_PER_OUTPUT_TOKEN
    token_usage = f"🔒 Token Usage: {total_token} (input: {input_token}; output: {output_token})"
    token_cost = f"💰 Token Cost: {total_cost:.2f} (USD)"

    return token_usage, token_cost


def format_summarized_transcripts(
        log_segment_name: str, content_text: dict):
    """
    Formats the given log segment name, and content transcripts into structured HTML output.

    Args:
        - log_segment_name (str): The name of the log segment.
        - content_text (dict): The content text dictionary.

    Returns:
        - subject_title (str): The subject of the ticket.
        - summerized_ticket_content (str): The summarized ticket content.
    """

    subject: str = content_text["subject"]
    content_transcripts: list = content_text["transcript"]

    transcript_output = ""

    for i in range(len(content_transcripts)):
        transcript_output += f"<blockquote><h3>Submitted by {content_transcripts[i]['submittedBy']}</h3>{content_transcripts[i]['content']}</blockquote>\n"

    subject_title = f"<h1>Subject: {subject}</h1>"
    summerized_ticket_content = f"<div>\n<h3>Case Name: {log_segment_name}</h3>\n{transcript_output}\n</div>"

    return subject_title, summerized_ticket_content


def extract_content_text(body: dict) -> dict:
    """
    Extracts the content text from the given body.
    The main goal is handling the JSON block in the content text.

    Args:
        - body (dict): A dictionary containing the content text.

    Returns:
        - content_text (dict): The content text dictionary.
    """

    content: str = body["content"][0]   # body["content"] is a list
    
    JSON_BLOCK_START    : str = "```json"
    BLOCK_START         : str = "```"
    BLOCK_END           : str = "```"
    JSON_BLOCK_START_LEN: int = len(JSON_BLOCK_START)
    BLOCK_START_LEN     : int = len(BLOCK_START)
    BLOCK_END_LEN       : int = len(BLOCK_END)

    if content["text"].startswith(JSON_BLOCK_START) and content["text"].endswith(BLOCK_END):
        content["text"] = content["text"][JSON_BLOCK_START_LEN: -BLOCK_END_LEN].strip()
    elif content["text"].startswith(BLOCK_START) and content["text"].endswith(BLOCK_END):
        content["text"] = content["text"][BLOCK_START_LEN: -BLOCK_END_LEN].strip()
    else:
        pass    # Do nothing

    content_text: dict = json.loads(content["text"])

    return content_text
