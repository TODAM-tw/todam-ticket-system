# ToDAM Ticket System   <!-- omit in toc -->

The frontend with gradio and combined with the API endpoints for the ticket system.

## Table of Contents   <!-- omit in toc -->
- [Developing Requirements](#developing-requirements)
- [Required Dependencies](#required-dependencies)
  - [Build `venv` for **MacOS**](#build-venv-for-macos)
  - [Build `venv` for **Windows**](#build-venv-for-windows)
  - [Run web app](#run-web-app)
- [Deployment](#deployment)
  - [Build the docker image](#build-the-docker-image)
  - [Deploy to AWS Lambda Function with AWS CDK](#deploy-to-aws-lambda-function-with-aws-cdk)
- [Project Structure](#project-structure)
  - [`app/`](#app)
    - [`app/cases/`](#appcases)
    - [`app/controllers/`](#appcontrollers)
    - [`app/infra/`](#appinfra)
    - [`app/views/`](#appviews)
  - [`docs/`](#docs)
  - [`scripts/`](#scripts)
- [Functions and Features](#functions-and-features)
  - [`app/infa/web/router.py`](#appinfawebrouterpy)
  - [Elements for the gradio app.](#elements-for-the-gradio-app)
    - [Blocks](#blocks)
    - [Header](#header)
    - [Refresh Button](#refresh-button)
    - [Log Segment ID Dropdown](#log-segment-id-dropdown)
  - [Past Model Output](#past-model-output)
    - [Example Response](#example-response)
    - [Method to process the Response](#method-to-process-the-response)
  - [Chat History Component](#chat-history-component)

## Developing Requirements

Python version `python3.11` or later with [`poetry`](https://python-poetry.org/) to manage the dependencies.

> [!IMPORTANT]
> If you have not installed `poetry`, please install it by following the [official guide](https://python-poetry.org/docs/#installation)

## Required Dependencies

- `gradio = "^4.31.0"`
- `uvicorn = "^0.29.0"`

### Build `venv` for **MacOS**
```shell
$ python3.11 -m venv venv
$ source venv/bin/activate
$ poetry install
$ rm -rf venv     # remove the venv
```

### Build `venv` for **Windows**
```shell
$ pip install virtualenv
$ virtualenv venv
$ venv\Scripts\activate
$ poetry install
$ rmdir /s venv     # remove the venv
```

### Run web app

Edit the `.env` file with your own token. Also need to follow the mode of the web app.

```shell
$ cp .env.example .env.<MODE>
```

```shell
# Ticket System Part
DEPARTMENT_ID="MSP_ID"

# API Endpoint Part
SUBMIT_TICKET_API_URL="DEPLOYED_SUBMIT_TICKET_API_URL"
LIST_LOG_SEGMENT_API_URL="DEPLOYED_LIST_LOG_SEGMENT_API_URL"
LIST_CHAT_HISTORY_API_URL="DEPLOYED_LIST_CHAT_HISTORY_API_URL"
BEDROCK_API_URL="DEPLOYED_BEDROCK_API_URL"

# AWS CDK Part
CDK_DEFAULT_ACCOUNT="YOUR_AWS_CDK_DEFAULT_ACCOUNT"
CDK_DEFAULT_REGION="YOUR_AWS_CDK_DEFAULT_REGION"
```

Run the web app with the following command.
```shell
# run the web app in development mode
$ python app.py --port 8080 --dev
# run the web app in test mode
$ python app.py --port 8080 --test
# run the web app in production mode
$ python app.py --port 8080 --prod

# Also you can customize the port number
$ python app.py --port 8081 --dev
```

> [!NOTE]
> If you want to run the app with the `uvicorn` server, so that you can design your own API and **reload** the app, you can run the following command.
> ```shell
> $ ./scripts/run.sh
> 
> # or
> $ uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
> ```
>
> This will use the `.env` as the default configuration file.

## Deployment

with `docker` installed, you can build and run the docker image.

### Build the docker image

```shell
$ docker build -t todam-ticket-system:<TAG_NAME> .

$ docker run -p 8080:8080 todam-ticket-system:<TAG_NAME>
```

### Deploy to AWS Lambda Function with AWS CDK

With the AWS CDK, you can deploy the gradio app to the AWS Lambda function. [^1]

```shell
$ cdk bootstrap
$ cdk deploy
```

## Project Structure

```shell
todam-ticket-system/
├── app/
├── docs/
├── scripts/
├── .env
├── docker-compose.yml
├── Dockerfile
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
└── requirements.txt
```

### `app/`

```shell
├── app/
│   ├── cases/
│   ├── controllers/
│   ├── infra/
│   ├── views/
│   ├── __init__.py
│   └── main.py
```

#### `app/cases/`

```shell
├── app/
│   ├── cases/
│   │   ├── __init__.py
│   │   ├── chat_history.py
│   │   ├── segment.py
│   │   ├── submit.py
│   │   └── ticket_summarized.py
```

#### `app/controllers/`

```shell
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── mock_ticket.py
```

#### `app/infra/`

```shell
├── app/
│   ├── infra/
│   │   ├── __init__.py
│   │   ├── db/
│   │   │   └── __init__.py
│   │   ├── web/
│   │   │   │   __init__.py
│   │   │   └── router.py
```

#### `app/views/`

```shell
├── app/
│   ├── views/
│   │   ├── components/
│   │   │   │   ...     # TODO
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   └── dashboard.py
```

### `docs/`

```shell
├── docs/
│   └── README.md
```

### `scripts/`

```shell
├── scripts/
│   └── run.sh
```

## Functions and Features

### `app/infa/web/router.py`

To mount the gradio app to the FastAPI, you can use the following code. Also include the mock ticket routes.

```python
import gradio as gr
from fastapi import FastAPI

from app.views.dashboard import build_playground
from app.controllers.mock_ticket import mock_ticket_routes


def setup_routers(app: FastAPI) -> None:
    gr.mount_gradio_app(app, build_playground(), path="/playground")
    
    app.include_router(mock_ticket_routes)
```

### Elements for the gradio app.

#### Blocks

The outermost container that can contain multiple `Component`.

```python
# app/views/dashboard.py
with gr.Blocks(
    title='ToDAM Ticket System',
) as demo:
```

#### Header

The header component that displays the title.

```python
# app/views/dashboard.py
gr.HTML(
    "<h1 align=center>ToDAM Ticket System</h1>"
)
```

#### Refresh Button

Once we launch the app, we need to fetch the data from the API endpoint. We can use the refresh button as a trigger to fetch the data. (Gradio needs the event to trigger the function; it does not have the `onload` event. Therefore, we need to use the refresh button to fetch the data.)

```python
# app/views/dashboard.py
refresh_btn = gr.Button(
    variant="secondary",
    value="🔄 Refresh Log Segments Records",
)
```

Once the user clicks the refresh button, it fetches the data from the API endpoint.

```python
# app/views/dashboard.py
refresh_btn.click(
    fn=get_segments,
    inputs=[log_segment_id],
    outputs=[log_segment_id],
)
```

The case of the refresh button is to fetch the data from the API endpoint. Then we will use the log segment ID to fetch the chat history. And make it to the format that we can display on the gradio app.

```python
# app/cases/segment.py
def get_segments(
        log_segment: gr.Dropdown) -> gr.Dropdown:
    """
    Get segments from the API

    Args:
        log_segment (gr.Dropdown): Dropdown object

    Returns:
        gr.Dropdown: Dropdown object
    """
    _ = load_dotenv(find_dotenv())
    list_log_segment_api_url: str = os.environ['LIST_LOG_SEGMENT_API_URL']

    payload = {}
    headers = {}

    response = requests.request(
        method="GET", url=list_log_segment_api_url, headers=headers, data=payload
    )
    if response.status_code == 200:
        data = json.loads(response.text)

    segment_ids = [segment["segment_id"] for segment in data["segments"]]
    segment_names = [segment["segment_name"] for segment in data["segments"]]
    group_ids = [segment["group_id"] for segment in data["segments"]]

    log_segment = gr.Dropdown(
        label="🚘 Log Segment Records (ID)",
        info="Select a Record Segment to summerize with 👇🏻",
        value=segment_ids[0],
        choices=segment_ids,
        interactive=True,
        multiselect=None,
        # visible=False,
    )

    return log_segment
```

#### Log Segment ID Dropdown

The dropdown component that allows the user to select the log segment ID. And it fetches the data from the API endpoint.

```python
# app/views/dashboard.py
log_segment_id = gr.Dropdown(
    label="🚘 Log Segment Records (ID)",
    info="Select a Record Segment to summerize with 👇🏻",
    interactive=True,
    multiselect=None,
    # visible=False,
)
```

Once the user selects the log segment ID, it fetches the data from the API endpoint.

```python
# app/views/dashboard.py
log_segment_id.change(
    fn=get_row_chat_history,
    inputs=log_segment_id,
    outputs=[row_chat_history, prev_summerized_ticket_content],
)
```

If the user selects the log segment ID, it fetches the chat history from the API endpoint. And ready to call the Azure ML API to get the summerized content.

```python
# app/cases/chat_history.py

# TODO:
# 1. 需要有能力去 Handle Dropdown 是空的情況 -> 具體要回傳什麼給 gradio
def get_row_chat_history(
        log_segment_subject: str) -> tuple[tuple[str, str], str]:
    _ = load_dotenv(find_dotenv())
    list_chat_history_api_url: str = os.environ['LIST_CHAT_HISTORY_API_URL']
    url = f"{list_chat_history_api_url}/messages?segment_id={log_segment_subject}"

    headers = {}
    payload = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = json.loads(response.text)

    messages = data["messages"]

    # print(data)

    row_chat_history = []

    for message in messages:
        if message["user_type"] == "Client":
            row_chat_history.append((None, message["content"]))
        elif message["user_type"] == "TAM":
            row_chat_history.append((message["content"], None))

    prev_summerized_ticket_content = """<img src="https://img.pikbest.com/png-images/20190918/cartoon-snail-loading-loading-gif-animation_2734139.png!f305cw" alt="cartoon snail loading" />"""

    return row_chat_history, prev_summerized_ticket_content

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
```

### Past Model Output

```python
def get_summarized_ticket_content(
        log_segment: gr.Dropdown, row_chat_history: gr.Chatbot) -> tuple[str, str]:
    _ = load_dotenv(find_dotenv())
    azure_ml_deployed_url : str = os.environ['AZURE_ML_DEPLOYED_URL']
    azure_ml_token        : str = os.environ['AZURE_ML_TOKEN']
    azure_model_deployment: str = os.environ['AZURE_MODEL_DEPLOYMENT']

    result = []
    current_user_type = None

    for item in row_chat_history:
        tam_message, client_message = item
        if tam_message:
            current_user_type = "TAM"
            content = tam_message
        elif client_message:
            current_user_type = "Client"
            content = client_message
        else:
            # Skip recording messages
            continue
        
        result.append({
            "user_type": current_user_type,
            "content": content
        })

    headers = {
        'azureml-model-deployment': azure_model_deployment,
        'authorization': f"Bearer {azure_ml_token}"
    }
    payload = str(result)

    response: Response = requests.request(
        "POST", azure_ml_deployed_url, 
        headers=headers, 
        data=payload
    )

    if response.status_code == 200:
        data: dict = json.loads(response.text)
    else:
        return "Error: Something went wrong with the API"

    result: dict = json.loads(data["result"])    # data["result"] 裡面是一個 JSON 格式的字串
    # transcript = result["transcript"]
    case_id = log_segment
    # case_id = result["caseId"]
    subject = result["subject"]

    transcript_output = ""
    for item in result['transcript']:
        transcript_output += f"<blockquote><h3>Submitted by {item['Submitted by']}</h3>Content: {item['content']}</blockquote>\n"

    subject_output = f"<h1>Subject: {subject}</h1>"
    summerized_ticket_content = f"<div>\n<h3>Case ID: {case_id}</h3>\n{transcript_output}\n</div>"
```

#### Example Response

```json
{
    "result": "{\n  \"subject\": \"Ticket regarding account upgrade\",\n  \"caseId\": null,\n  \"startDate\": null,\n  \"transcript\": [\n    {\n      \"Submitted by\": \"Customer\",\n      \"content\": \"Hello, I am having trouble upgrading my account to the premium plan. Every time I try to upgrade, it gives me an error message.\"\n    },\n    {\n      \"Submitted by\": \"TAM\",\n      \"content\": \"I apologize for the inconvenience. Can you please provide me with the exact error message you are receiving when trying to upgrade?\"\n    },\n    {\n      \"Submitted by\": \"Customer\",\n      \"content\": \"The error message says 'Payment Failed. Please check your payment details and try again.' But I have checked my payment details and they are correct.\"\n    },\n    {\n      \"Submitted by\": \"TAM\",\n      \"content\": \"Thank you for providing the error message. Let me investigate this issue further for you. Can you please provide me with your account username or email address?\"\n    },\n    {\n      \"Submitted by\": \"Customer\",\n      \"content\": \"My account username is john123.\"\n    },\n    {\n      \"Submitted by\": \"TAM\",\n      \"content\": \"Thank you for the information. I will look into your account and see what might be causing the payment failure. Please bear with me for a moment.\"\n    }\n  ]\n}"
}
```

#### Method to process the Response

1. Extract `result` from the response. (The `result` is a JSON string.)

```python
if response.status_code == 200:
    data: dict = json.loads(response.text)
else:
    return "Error: Something went wrong with the API"

result: dict = json.loads(data["result"])    # data["result"] 裡面是一個 JSON 格式的字串
```

2. Extract the `subject` from the `result`.

```python
subject = result["subject"]
```

3. Extract the `transcript` from the `result` and get the `Submitted by` and `content`.

```python
transcript_output = ""
for item in result['transcript']:
    transcript_output += f"<blockquote><h3>Submitted by {item['Submitted by']}</h3>Content: {item['content']}</blockquote>\n"
```

### Chat History Component

```python
(None, "Customer sayings")
("TAM sayings", None)
```



```json
{
    "id": "msg_016YsKtQJGV1BTkdujPsWyhh",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "{\n  \"subject\": \"Azure Linux VM 504 Error and Performance Optimization\",\n  \"caseId\": null,\n  \"startDate\": null,\n  \"transcript\": [\n    {\n      \"submittedBy\": \"Client\",\n      \"content\": \"我們的虛擬機器在 Azure 上運行，配置為 Linux，VM 世代為 V1，架構是 x64，休眠已禁用，公共 IP 地址為 20.253.222.207（網絡接口為 adam-linux580），私有 IP 地址為 10.0.3.4，虛擬網絡/子網絡為 adam-vnet/adam-private-1，規模為標準 B2s（2 vCPUs、4 GiB RAM），磁盤為 adam-disk-linux（主機加密已禁用，未啟用 Azure 磁盤加密），安全類型為標準。我們最近遇到了 504 錯誤，您能幫忙分析問題所在嗎？\"\n    },\n    {\n      \"submittedBy\": \"Client\",\n      \"content\": \"[Image URL](        https://todam-bucket-478977890696-us-east-1.s3.amazonaws.com/jpg/test_azure.png)\\nThe image shows the configuration details of a virtual machine (VM) running on a cloud platform, likely Microsoft Azure.\"\n    },\n    {\n      \"submittedBy\": \"TAM\",\n      \"content\": \"很抱歉聽到您遇到 504 錯誤。這可能與您的虛擬機器的性能或連接有關。請確保您的虛擬機器的資源使用合理並且未受到任何限制，特別是在高負載時。同時，請檢查您的網絡設置，確保連接到 Azure 的網絡穩定且無阻礙。您可以查看 Azure 的監控工具來檢視虛擬機器的性能指標和網絡狀態。如果問題仍然存在，您可能需要進一步的調查或聯繫 Azure 技術支援以獲得協助。\"\n    },\n    {\n      \"submittedBy\": \"Client\",\n      \"content\": \"感謝您的回答。我們將按照您提供的建議來檢查和解決問題。另外，我們還有一個關於虛擬機器性能調整的問題。我們的 VM 在高負載時表現不佳，您能提供一些性能優化的建議嗎？\"\n    },\n    {\n      \"submittedBy\": \"TAM\",\n      \"content\": \"當虛擬機器在高負載時表現不佳時，您可以考慮以下幾點來進行性能優化：首先，檢查虛擬機器的資源配置，可能需要增加 vCPU 和 RAM 來應對更高的負載；其次，優化應用程序和服務，確保它們能夠有效地利用虛擬機器的資源；另外，可以考慮使用 Azure 的負載均衡器來平衡負載，將流量分配到多個虛擬機器上。最後，監控系統性能並進行持續的優化和調整以確保最佳效能。\"\n    }\n  ]\n}"
        }
    ],
    "model": "claude-3-sonnet-28k-20240229",
    "stop_reason": "end_turn",
    "stop_sequence": null,
    "usage": {
        "input_tokens": 1578,
        "output_tokens": 915
    }
}
```

```json
{
    "subject": "Azure Linux VM 504 Error and Performance Optimization",
    "caseId": null,
    "startDate": null,
    "transcript": [
        {
            "submittedBy": "Client",
            "content": "我們的虛擬機器在 Azure 上運行，配置為 Linux，VM 世代為 V1，架構是 x64，休眠已禁用，公共 IP 地址為 20.253.222.207（網絡接口為 adam-linux580），私有 IP 地址為 10.0.3.4，虛擬網絡/子網絡為 adam-vnet/adam-private-1，規模為標準 B2s（2 vCPUs、4 GiB RAM），磁盤為 adam-disk-linux（主機加密已禁用，未啟用 Azure 磁盤加密），安全類型為標準。我們最近遇到了 504 錯誤，您能幫忙分析問題所在嗎？"
        },
        {
            "submittedBy": "Client",
            "content": "[Image URL](
        https://todam-bucket-478977890696-us-east-1.s3.amazonaws.com/jpg/test_azure.png)\nThe
        image shows the configuration details of a virtual machine (VM) running on a cloud platform, likely Microsoft Azure."
        },
        {
            "submittedBy": "TAM",
            "content": "很抱歉聽到您遇到 504 錯誤。這可能與您的虛擬機器的性能或連接有關。請確保您的虛擬機器的資源使用合理並且未受到任何限制，特別是在高負載時。同時，請檢查您的網絡設置，確保連接到 Azure 的網絡穩定且無阻礙。您可以查看 Azure 的監控工具來檢視虛擬機器的性能指標和網絡狀態。如果問題仍然存在，您可能需要進一步的調查或聯繫 Azure 技術支援以獲得協助。"
        },
        {
            "submittedBy": "Client",
            "content": "感謝您的回答。我們將按照您提供的建議來檢查和解決問題。另外，我們還有一個關於虛擬機器性能調整的問題。我們的 VM 在高負載時表現不佳，您能提供一些性能優化的建議嗎？"
        },
        {
            "submittedBy": "TAM",
            "content": "當虛擬機器在高負載時表現不佳時，您可以考慮以下幾點來進行性能優化：首先，檢查虛擬機器的資源配置，可能需要增加 vCPU 和 RAM 來應對更高的負載；其次，優化應用程序和服務，確保它們能夠有效地利用虛擬機器的資源；另外，可以考慮使用 Azure 的負載均衡器來平衡負載，將流量分配到多個虛擬機器上。最後，監控系統性能並進行持續的優化和調整以確保最佳效能。"
        }
    ]
}
```


[^1]: [Serverless Machine Learning Applications with Hugging Face Gradio and AWS Lambda](https://www.philschmid.de/serverless-gradio)
[^2]: [philschmid/serverless-machine-learning/gradio-aws-lambda-transformers](https://github.com/philschmid/serverless-machine-learning/tree/main/gradio-aws-lambda-transformers)


