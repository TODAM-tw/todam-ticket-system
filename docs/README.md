# ToDAM Ticket System

The frontend with gradio and combined with the API endpoints for the ticket system.

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

Edit the `.env` file with your own token.

```shell
$ cp .env.example .env
```

```shell
# Azure ML Part
AZURE_ML_TOKEN="YOUR_AZURE_ML_TOKEN"
AZURE_ML_DEPLOYED_URL="YOUR_AZURE_ML_DEPLOYED_URL"
AZURE_MODEL_DEPLOYMENT="YOUR_AZURE_MODEL_DEPLOYMENT"

# Ticket System Part
DEPARTMENT_ID="MSP_ID"

# API Endpoint
SUBMIT_TICKET_API_URL="DEPLOYED_SUBMIT_TICKET_API_URL"
LIST_LOG_SEGMENT_API_URL="DEPLOYED_LIST_LOG_SEGMENT_API_URL"
LIST_CHAT_HISTORY_API_URL="DEPLOYED_LIST_CHAT_HISTORY_API_URL"
```

Run the web app with the following command.
```shell
$ ./scripts/run.sh
```

## Deployment

with `docker` and `docker-compose` installed, you can build and run the docker image.

### Build the docker image

```shell
$ docker build -t todam-ticket-system:<TAG_NAME> .

$ docker run -p 8080:8080 todam-ticket-system:<TAG_NAME>
```

### Run the docker container
```shell
# build the docker image and run the container
$ docker-compose up -d
# follow the logs
$ docker-compose logs -f
# stop the container but keep the container
$ docker-compose stop
# stop the container and discard the container
$ docker-compose down
```

### Upload the docker image to AWS ECR

```shell
$ aws ecr ...   # TODO
```

### Deploy the docker container to AWS ECS

```shell
$ aws ecs ...   # TODO
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
│   │   └── summerized_content.py
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

