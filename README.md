# ToDAM Ticket System

<img align=center alt="TODAM Ticket System" src="./docs/imgs/cover.png">

The frontend with gradio and combined with the API endpoints for the ticket system.

## Developing Requirements

Python version `python3.11` or later with [`poetry`](https://python-poetry.org/) to manage the dependencies.

> [!IMPORTANT]
> If you have not installed `poetry`, please install it by following the [official guide](https://python-poetry.org/docs/#installation)

## Required Dependencies

- `gradio = "^4.31.0"`
- `uvicorn = "^0.29.0"`
- `aws-cdk-lib = "^2.141.0"`
- `constructs = "^10.3.0"`
- `mangum = "^0.17.0"`

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

```shell
$ cdk bootstrap
$ cdk deploy
```

## CONTACT INFO.

> Cloud Engineer Intern </br>
> **Hugo ChunHo Lin**
> 
> <aside>
>   📩 E-mail: <a href="mailto:hugo970217@gmail.com">hugo970217@gmail.com</a>
> <br>
>   📩 ECV E-mail: <a href="mailto:hugo.lin@ecloudvalley.com">hugo.lin@ecloudvalley.com</a>
> <br>
>   🧳 Linkedin: <a href="https://www.linkedin.com/in/1chooo/">Hugo ChunHo Lin</a>
> <br>
>   👨🏻‍💻 GitHub: <a href="https://github.com/1chooo">1chooo</a>
>    
> </aside>

## License
Released under [Apache License](./LICENSE) by [TODAM-tw](https://github.com/TODAM-tw).

