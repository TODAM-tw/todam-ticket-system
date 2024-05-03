import json

payload = [
    {
        "user_type": "TAM",
        "content": "start recording"
    },
    {
        "user_type": "TAM",
        "content": "start recording"
    }
]

print(str(payload))

import requests

url = "https://todam-aml-workspace-dev.eastus2.inference.ml.azure.com/score"

# payload = "{\r\n    \"input\": {\r\n        \"question\": \"TAM: start recording\\nTAM: start recording\\nTAM: start recording\\nTAM: end recording\\nTAM: TAM這是一則來自TAM的訊息\\nClient: Client這是一則來自客戶的訊息\\nClient: Client這是一則來自客戶的訊息\\nTAM: end recording\\nTAM: end recording\\nTAM: TAM這是一則來自TAM的訊息\"\r\n    }\r\n}"
headers = {
  'azureml-model-deployment': 'todam-aml-workspace-dev-0503-v1',
  'authorization': "Bearer HWMJEYWdrSFY7YFx7vZGUi3ptfiWBk6O"
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

data = json.loads(response.text)

# 提取 result 鍵對應的值
result_string = data["result"]

# 再次將 result 的值轉換為字典
result_dict = json.loads(result_string)

# 顯示轉換後的結果
print(result_dict)


data = [('start recording', None), ('start recording', None), ('start recording', None), ('end recording', None), ('TAM這是一則來自TAM的訊息', None), (None, 'Client這是一則來自客戶的訊息'), (None, 'Client這是一則來自客戶的訊息'), ('end recording', None), ('end recording', None), ('TAM這是一則來自TAM的訊息', None)]

result = []
current_user_type = None

for item in data:
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

print(result)

payload = str(result)

url = "https://todam-aml-workspace-dev.eastus2.inference.ml.azure.com/score"

# payload = "{\r\n    \"input\": {\r\n        \"question\": \"TAM: start recording\\nTAM: start recording\\nTAM: start recording\\nTAM: end recording\\nTAM: TAM這是一則來自TAM的訊息\\nClient: Client這是一則來自客戶的訊息\\nClient: Client這是一則來自客戶的訊息\\nTAM: end recording\\nTAM: end recording\\nTAM: TAM這是一則來自TAM的訊息\"\r\n    }\r\n}"
headers = {
    'azureml-model-deployment': 'todam-aml-workspace-dev-0503-v1',
    # 'authorization': f"Bearer {os.getenv('AZURE_ML_TOKEN')}"
    'authorization': "Bearer HWMJEYWdrSFY7YFx7vZGUi3ptfiWBk6O"
    }

response = requests.request("POST", url, headers=headers, data=payload)

data = json.loads(response.text)

print(data)

print(data["result"])


result = json.loads(data["result"])
transcript = result["transcript"]

print(transcript)

markdown_output = ""

for item in result['transcript']:
    markdown_output += "```\nSubmitted by {}\nContent: {}\n```\n\n".format(item['Submitted by'], item['content'])

print(markdown_output)