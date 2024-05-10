import os

from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())

azure_ml_deployed_url = os.environ['AZURE_ML_DEPLOYED_URL']
azure_ml_token = os.environ['AZURE_ML_TOKEN']
