# Line Bot Logger

## User Info Log

```json
[
    {
        "display_name": "User",
        "language": "en",
        "picture_url": "https://example.com/profile_picture",
        "status_message": null,
        "user_id": "user_id"
    },
    {
        "display_name": "User",
        "language": "en",
        "picture_url": "https://example.com/profile_picture",
        "status_message": null,
        "user_id": "user_id"
    }
]
```

### How to extract the value from the User Log?

- `display_name: str`
- `language: str`
- `picture_url: str`
- `status_message: str`
- `user_id: str`

```python
def get_user_infos() -> list | str:
    response: Response = requests.get(f"http://{host_name}:{port_number}/user/")
    if response.status_code == 200:
        user_infos = json.loads(response.text)
        return user_infos
    else:
        return "Error fetching data from URL"

user_infos: list = get_user_infos()

for i in range(len(user_infos)):
    user_infos_dict = json.loads(user_infos[i])
    try:
        display_name  : str = user_infos_dict['display_name']
        language      : str = user_infos_dict['evelanguagents']
        picture_url   : str = user_infos_dict['picture_url']
        status_message: str = user_infos_dict['status_message']
        user_id       : str = user_infos_dict['user_id']
    except Exception as e:
        print("Error: ", e)
```

## User Event Log (Personal)

```json
[
    {
        "destination": "destination",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "id",
                    "quoteToken": "quote_token",
                    "text": "text_content"
                },
                "webhookEventId": "webhook_event_id",
                "deliveryContext": {
                    "isRedelivery": false
                },
                "timestamp": number_of_timestamp,
                "source": {
                    "type": "user",
                    "userId": "user_id"
                },
                "replyToken": "reply_token",
                "mode": "active"
            }
        ]
    },
    {
        "destination": "destination",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "id",
                    "quoteToken": "quote_token",
                    "text": "text_content"
                },
                "webhookEventId": "webhook_event_id",
                "deliveryContext": {
                    "isRedelivery": false
                },
                "timestamp": number_of_timestamp,
                "source": {
                    "type": "user",
                    "userId": "user_id"
                },
                "replyToken": "reply_token",
                "mode": "active"
            }
        ]
    }
]
```

### How to extract the value from the User Event Log (Personal)?

- `destination: str`
- `event_type: str`
- `event_message_type: str`
- `event_message_id: str`
- `event_message_quote_token: str`
- `event_message_text: str`
- `event_webhook_event_id: str`
- `event_is_redelivery: bool`
- `event_timestamp: int`
- `event_source_type: str`
- `event_source_user_id: str`
- `event_reply_token: str`
- `event_mode: str`

```python
def get_event_logs_infos() -> list | str:
    response: Response = requests.get(f"http://{host_name}:{port_number}/logs/event/{date}")
    if response.status_code == 200:
        event_logs_infos = json.loads(response.text)
        return event_logs_infos
    else:
        return "Error fetching data from URL"

event_logs_infos: list = get_event_logs_infos()

for i in range(len(event_logs_infos)):
    event_logs_infos_dict = json.loads(user_infos[i])
    try:
        destination              : str = event_logs_infos_dict['destination']
        event_type               : str = event_logs_infos_dict['events'][0]["type"]
        event_message_type       : str = event_logs_infos_dict['events'][0]["message"]["type"]
        event_message_id         : str = event_logs_infos_dict['events'][0]["message"]["id"]
        event_message_quote_token: str = event_logs_infos_dict['events'][0]["message"]["quoteToken"]
        event_message_text       : str = event_logs_infos_dict['events'][0]["message"]["text"]
        event_webhook_event_id   : str = event_logs_infos_dict['events'][0]["webhookEventId"]
        event_is_redelivery      : bool = event_logs_infos_dict['events'][0]["deliveryContext"]["isRedelivery"]
        event_timestamp          : int = event_logs_infos_dict['events'][0]["timestamp"]
        event_source_type        : str = event_logs_infos_dict['events'][0]["source"]["type"]
        event_source_user_id     : str = event_logs_infos_dict['events'][0]["source"]["userId"]
        event_reply_token        : str = event_logs_infos_dict['events'][0]["replyToken"]
        event_mode               : str = event_logs_infos_dict['events'][0]["mode"]
    except Exception as e:
        print("Error: ", e)
```

## User Event Log (Group)

```json
[
    {
        "destination": "destination",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "id",
                    "quoteToken": "quote_token",
                    "text": "text_content"
                },
                "webhookEventId": "webhook_event_id",
                "deliveryContext": {
                    "isRedelivery": false
                },
                "timestamp": number_of_timestamp,
                "source": {
                    "type": "user",
                    "groupId": "group_id",
                    "userId": "user_id"
                },
                "replyToken": "reply_token",
                "mode": "active"
            }
        ]
    },
    {
        "destination": "destination",
        "events": [
            {
                "type": "message",
                "message": {
                    "type": "text",
                    "id": "id",
                    "quoteToken": "quote_token",
                    "text": "text_content"
                },
                "webhookEventId": "webhook_event_id",
                "deliveryContext": {
                    "isRedelivery": false
                },
                "timestamp": number_of_timestamp,
                "source": {
                    "type": "user",
                    "groupId": "group_id",
                    "userId": "user_id"
                },
                "replyToken": "reply_token",
                "mode": "active"
            }
        ]
    }
]
```

### How to extract the value from the User Event Log (Group)?

- `destination: str`
- `event_type: str`
- `event_message_type: str`
- `event_message_id: str`
- `event_message_quote_token: str`
- `event_message_text: str`
- `event_webhook_event_id: str`
- `event_is_redelivery: bool`
- `event_timestamp: int`
- `event_source_type: str`
- `event_source_group_id: str`
- `event_source_user_id: str`
- `event_reply_token: str`
- `event_mode: str`

```python
def get_event_logs_infos() -> list | str:
    response: Response = requests.get(f"http://{host_name}:{port_number}/logs/event/{date}")
    if response.status_code == 200:
        event_logs_infos = json.loads(response.text)
        return event_logs_infos
    else:
        return "Error fetching data from URL"

event_logs_infos: list = get_event_logs_infos()

for i in range(len(event_logs_infos)):
    event_logs_infos_dict = json.loads(user_infos[i])
    try:
        destination              : str = event_logs_infos_dict['destination']
        event_type               : str = event_logs_infos_dict['events'][0]["type"]
        event_message_type       : str = event_logs_infos_dict['events'][0]["message"]["type"]
        event_message_id         : str = event_logs_infos_dict['events'][0]["message"]["id"]
        event_message_quote_token: str = event_logs_infos_dict['events'][0]["message"]["quoteToken"]
        event_message_text       : str = event_logs_infos_dict['events'][0]["message"]["text"]
        event_webhook_event_id   : str = event_logs_infos_dict['events'][0]["webhookEventId"]
        event_is_redelivery      : bool = event_logs_infos_dict['events'][0]["deliveryContext"]["isRedelivery"]
        event_timestamp          : int = event_logs_infos_dict['events'][0]["timestamp"]
        event_source_type        : str = event_logs_infos_dict['events'][0]["source"]["type"]
        event_source_group_id    : str = event_logs_infos_dict['events'][0]["source"]["groupId"]
        event_source_user_id     : str = event_logs_infos_dict['events'][0]["source"]["userId"]
        event_reply_token        : str = event_logs_infos_dict['events'][0]["replyToken"]
        event_mode               : str = event_logs_infos_dict['events'][0]["mode"]
    except Exception as e:
        print("Error: ", e)
```

## Follow

```json
{
    "destination": "destination",
    "events": [
        {
            "type": "unfollow",
            "webhookEventId": "webhook_event_id",
            "deliveryContext": {
                "isRedelivery": false
            },
            "timestamp": timestamp,
            "source": {
                "type": "user",
                "userId": "user_id"
            },
            "mode": "active"
        }
    ]
}
```

## Unfollow

```json
{
    "destination": "destination",
    "events": [
        {
            "type": "unfollow",
            "webhookEventId": "webhook_event_id",
            "deliveryContext": {
                "isRedelivery": false
            },
            "timestamp": timestamp,
            "source": {
                "type": "user",
                "userId": "user_id"
            },
            "mode": "active"
        }
    ]
}
```

## Reference

### JSON

- [Json.cn](http://www.json.cn/)
