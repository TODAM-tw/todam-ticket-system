import os

import requests
from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

azure_ml_deployed_url = os.environ['AZURE_ML_DEPLOYED_URL']
azure_ml_token = os.environ['AZURE_ML_TOKEN']
azure_model_deployment = os.environ['AZURE_MODEL_DEPLOYMENT']

print(azure_ml_deployed_url)
print(azure_ml_token)
print(azure_model_deployment)

payload = "{\r\n    \"input\": {\r\n        \"question\": \"TAM: start recording\\nTAM: start recording\\nTAM: start recording\\nTAM: end recording\\nTAM: TAM這是一則來自TAM的訊息\\nClient: Client這是一則來自客戶的訊息\\nClient: Client這是一則來自客戶的訊息\\nTAM: end recording\\nTAM: end recording\\nTAM: TAM這是一則來自TAM的訊息\"\r\n    }\r\n}"
headers = {
    'azureml-model-deployment': azure_model_deployment,
    'authorization': f"Bearer {azure_ml_token}"
}

response = requests.request("POST", azure_ml_deployed_url, headers=headers, data=payload)

print(response.text)
