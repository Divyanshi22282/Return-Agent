import os
from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

easypost_api_key = os.getenv("EASYPOST_API_KEY")
fedex_api_key = os.getenv("FEDEX_API_KEY")
fedex_api_secret = os.getenv("FEDEX_API_SECRET")
fedex_account_number = os.getenv("FEDEX_ACCOUNT_NUMBER")
ryder_api_key = os.getenv("RYDER_API_KEY")
ryder_api_secret = os.getenv("RYDER_API_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
client = OpenAI(api_key=OPENAI_API_KEY)

# MongoDB
MONGODB_URI = os.getenv("MONGODB_URI")
mongo = MongoClient(MONGODB_URI)
db = mongo["ekyam_test_ai_agents_db"]

# MongoDB Collections
collection = db["CustomerOrderItem"]
returns_col = db["returnorders"]
fulfill_col = db["OrderFullfillments"]
inventory_col = db["InventoryRecords"]
address_col = db["CustomerOrdersAddress"]

# OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)
