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
