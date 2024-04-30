import gradio as gr
import requests
from requests.models import Response

# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio

def get_log_segment(log_segment):

    segments = {
        "segments": [
            {
                "segment_id": "segment_id_0001",
                "segment_name": "segment_0001",
                "group_id": "group_id_0001"
            },
            {
                "segment_id": "segment_id_0002",
                "segment_name": "segment_0002",
                "group_id": "grooup_id_0002"
            },
            {
                "segment_id": "segment_id_0003",
                "segment_name": "segment_0003",
                "group_id": "group_id_0001"
            },
            {
                "segment_id": "segment_id_0004",
                "segment_name": "segment_0004",
                "group_id": "grooup_id_0002"
            }
        ]
    }

    # response: Response = requests.get(f"http://0.0.0.0:8080/mock_ticket?id=1")

    response = segments

    segment_names = [segment["segment_name"] for segment in response["segments"]]
    segment_ids = [segment["segment_id"] for segment in response["segments"]]

    print(segment_names)

    log_segment = gr.Dropdown(
        label="🚘 Log Segment Records",
        info="Select a Record Segment to summerize with 👇🏻",
        value=segment_ids[0],
        choices=segment_ids,
        interactive=True,
        multiselect=None,
    )

    row_chat_history = (("Hi", "Hello"), ("How are you?", "I am fine, thank you!"), ("HiHI", None), ("HelloHello", None))

    summerized_ticket_conent = "This is a summerized ticket content."

    return log_segment, row_chat_history, summerized_ticket_conent
    

def render_logs_summerized_tickets(
        log_segment_subject: str) -> tuple[tuple[str, str], str]:
    if log_segment_subject == "segment_id_0001":
        row_chat_history_segment = get_row_chat_history_segment("segment_id_0001")
        row_chat_history = process_tickets(row_chat_history_segment["Tickets"])
        summerized_ticket_conent = summerized_by_model(row_chat_history_segment)
    elif log_segment_subject == "segment_id_0002":
        row_chat_history_segment = get_row_chat_history_segment("segment_id_0002")
        row_chat_history = process_tickets(row_chat_history_segment["Tickets"])
        summerized_ticket_conent = summerized_by_model(row_chat_history_segment)
    elif log_segment_subject == "segment_id_0003":
        row_chat_history_segment = get_row_chat_history_segment("segment_id_0003")
        row_chat_history = process_tickets(row_chat_history_segment["Tickets"])
        summerized_ticket_conent = summerized_by_model(row_chat_history_segment)
    elif log_segment_subject == "segment_id_0004":
        row_chat_history_segment = get_row_chat_history_segment("segment_id_0004")
        row_chat_history = process_tickets(row_chat_history_segment["Tickets"])
        summerized_ticket_conent = summerized_by_model(row_chat_history_segment)

    return row_chat_history, summerized_ticket_conent

def summerized_by_model(row_chat_history_segment):
    return f"""\
{row_chat_history_segment}
"""


def process_tickets(tickets):
    processed_tickets = []
    for ticket in tickets:
        role = ticket.get("Role")
        description = ticket.get("Description")
        if role == "Client":
            processed_tickets.append((None, description))
        elif role == "TAM":
            processed_tickets.append((description, None))
    return processed_tickets

def get_row_chat_history_segment(segment_id: str):
    if segment_id == "segment_id_0001":
        return {
            "Service": "Technical",
            "Category": "Lambda",
            "Client": "1234",
            "Tickets": [
                {
                    "Role": "Client",
                    "Description": "Our AWS Lambda function is failing to execute properly. It's triggered by S3 uploads, but we're experiencing intermittent failures. We've checked the function configuration and event source mappings, but the issue persists. We need assistance to diagnose and resolve this problem."
                },
                {
                    "Role": "TAM",
                    "Description": "Reviewed the reported issue with the Lambda function. Here's the plan to address the problem:"
                },
                {
                    "Role": "TAM",
                    "Description": "1. Function Configuration Check:\n- Verify the function configuration settings, including timeout, memory allocation, and IAM roles.\n- Review the CloudWatch logs for any error messages or warnings during function invocation."
                },
                {
                    "Role": "TAM",
                    "Description": "2. Event Source Mapping Analysis:\n- Check the event source mappings for the Lambda function to ensure proper integration with S3.\n- Monitor S3 bucket notifications for any delays or errors."
                },
                {
                    "Role": "Client",
                    "Description": "We'll proceed with the troubleshooting steps outlined. We've checked the function configuration, but the issue persists. We'll provide access to the CloudWatch logs for further analysis."
                },
                {
                    "Role": "TAM",
                    "Description": "Could you provide access to the CloudWatch logs for the Lambda function? Additionally, please share any specific error messages observed during the function execution."
                }
            ]
        }
    elif segment_id == "segment_id_0002":
        return {
            "Service": "Technical",
            "Category": "Simple Storage Service (S3)",
            "Client": "5678",
            "Tickets": [
                {
                    "Role": "Client",
                    "Description": "We're encountering issues with our AWS S3 bucket. Some objects are not accessible, and we're getting access denied errors. We've checked the bucket policies and permissions, but the issue persists. Urgently need assistance to restore access to the affected objects."
                },
                {
                    "Role": "TAM",
                    "Description": "Reviewed the reported issue with the S3 bucket. Here's the plan to address the problem:"
                },
                {
                    "Role": "TAM",
                    "Description": "1. Bucket Policy Review:\n- Review the bucket policies to ensure proper permissions are configured for object access.\n- Check for any deny policies that might be restricting access to the affected objects."
                },
                {
                    "Role": "TAM",
                    "Description": "2. Object Metadata Check:\n- Verify the metadata of the affected objects, including ACLs and object ownership.\n- Ensure proper versioning and encryption settings are enabled for the objects."
                },
                {
                    "Role": "Client",
                    "Description": "We'll proceed with the troubleshooting steps outlined. We've reviewed the bucket policies, but the issue persists. We'll provide access to the affected object metadata for further analysis."
                },
                {
                    "Role": "TAM",
                    "Description": "Could you provide access to the metadata of the affected objects in the S3 bucket? Additionally, please share any specific error messages encountered when accessing the objects."
                }
            ]
        }
    elif segment_id == "segment_id_0003":
        return {
            "Service": "Technical",
            "Category": "AWS EC2",
            "Client": "91011",
            "Tickets": [
                {
                    "Role": "Client",
                    "Description": "One of our AWS EC2 instances is experiencing performance degradation. It's running a critical application, and the response times have significantly increased. We've checked the instance status and CPU utilization, but haven't been able to identify the cause. We need immediate assistance to restore the performance of the instance."
                },
                {
                    "Role": "TAM",
                    "Description": "Reviewed the reported issue with the EC2 instance. Here's the plan to address the problem:"
                },
                {
                    "Role": "TAM",
                    "Description": "1. Instance Health Check:\n- Conduct a thorough health check of the EC2 instance, including CPU, memory, and disk utilization.\n- Monitor system metrics for any resource bottlenecks or performance issues."
                },
                {
                    "Role": "TAM",
                    "Description": "2. Application Profiling:\n- Analyze the application running on the EC2 instance to identify any performance bottlenecks.\n- Check for any long-running processes or high resource usage."
                },
                {
                    "Role": "Client",
                    "Description": "We'll proceed with the troubleshooting steps outlined. We've checked the instance health metrics, but the issue persists. We'll provide access to the system logs for further analysis."
                },
                {
                    "Role": "TAM",
                    "Description": "Could you provide access to the CloudWatch metrics and detailed system logs for the EC2 instance? Additionally, please share any specific symptoms or errors observed during the performance degradation."
                }
            ]
        }
    elif segment_id == "segment_id_0004":
        return {
            "Service": "Technical",
            "Category": "Lambda",
            "Client": "2468",
            "Tickets": [
                {
                    "Role": "Client",
                    "Description": "We've encountered an issue with our AWS Lambda function. It's not processing incoming events from our DynamoDB stream. We've checked the function configuration and event source mappings, but the function is not triggered. We require assistance to diagnose and resolve this issue promptly."
                },
                {
                    "Role": "TAM",
                    "Description": "Acknowledged the reported issue with the Lambda function. Here's the plan to address the problem:"
                },
                {
                    "Role": "TAM",
                    "Description": "1. Event Source Mapping Validation:\n- Verify the event source mapping configuration for the Lambda function and DynamoDB stream.\n- Check for any errors in the CloudWatch logs related to event processing failures."
                },
                {
                    "Role": "TAM",
                    "Description": "2. Function Configuration Review:\n- Review the function permissions and resource policies to ensure proper access to the DynamoDB stream.\n- Monitor AWS CloudTrail logs for any unauthorized API calls or permission issues."
                },
                {
                    "Role": "Client",
                    "Description": "We'll proceed with the troubleshooting steps outlined. We've reviewed the event source mapping, but the issue persists. We'll provide access to the CloudWatch logs for further analysis."
                },
                {
                    "Role": "TAM",
                    "Description": "Could you provide access to the CloudWatch logs for the Lambda function? Additionally, please share any specific error messages observed during the event processing."
                }
            ]
        }
    else:
        return {}







if __name__ == "__main__":
    get_log_segment()
