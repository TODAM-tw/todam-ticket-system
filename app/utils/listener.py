from app.cases.chat_history import get_row_chat_history
from app.cases.segment import get_segment_names
from app.cases.submit import send_summarized_ticket_content
from app.cases.ticket_summarized import get_summarized_ticket_content
from app.utils.update import render_preview


def background_listener(
        refresh_btn, log_segment_name, 
        id_name_comparison, row_chat_history, 
        message_type, summarized_ticket_conent, 
        preview_summarized_ticket_subject, 
        preview_summarized_ticket_content, 
        token_usage, token_cost, 
        regenerate_summarized_ticket_content_btn, 
        submit_summarized_btn, submit_status
    ) -> None:
    """
    Listen to the changes in the UI and trigger the appropriate functions
    
    Args:
        - refresh_btn (gr.Button): The refresh button
        - log_segment_name (gr.Select): The log segment name
        - id_name_comparison (gr.Hidden): The hidden field for the comparison
        - row_chat_history (gr.Chatbot): The chat history row data
        - message_type (gr.Hidden): The hidden field for the message type
        - summarized_ticket_conent (gr.Textbox): The summarized ticket content
        - preview_summarized_ticket_subject (gr.HTML): The preview of the summarized ticket subject
        - preview_summarized_ticket_content (gr.HTML): The preview of the summarized ticket content
        - token_usage (gr.ProgressBar): The token usage
        - token_cost (gr.ProgressBar): The token cost
        - regenerate_summarized_ticket_content_btn (gr.Button): The regenerate button
        - submit_summarized_btn (gr.Button): The submit button
        - submit_status (gr.ProgressBar): The submit status

    Returns:
        - None
    """
    refresh_btn.click(
        fn=get_segment_names,
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
        outputs=preview_summarized_ticket_content,
    )

    row_chat_history.change(
        fn=get_summarized_ticket_content,
        inputs=[log_segment_name, row_chat_history, message_type],
        outputs=[
            preview_summarized_ticket_subject, preview_summarized_ticket_content, 
            summarized_ticket_conent, token_usage, token_cost
        ],
    )

    regenerate_summarized_ticket_content_btn.click(
        fn=get_summarized_ticket_content,
        inputs=[log_segment_name, row_chat_history, message_type],
        outputs=[
            preview_summarized_ticket_subject, preview_summarized_ticket_content, 
            summarized_ticket_conent, token_usage, token_cost
        ],
    )

    submit_summarized_btn.click(
        fn=send_summarized_ticket_content,
        inputs=[
            preview_summarized_ticket_subject, summarized_ticket_conent, 
            log_segment_name, id_name_comparison,
        ],
        outputs=submit_status,
    )
