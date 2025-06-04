# services/return_policy.py

from openai import OpenAI
import os
from dotenv import load_dotenv
from pymongo import MongoClient
import re

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
mongo = MongoClient(os.getenv("MONGODB_URI"))
db = mongo["ekyam_test_ai_agents_db"]
collection = db["CustomerOrderItem"]

async def process_return_policy_change(prompt: str):
    system_prompt = (
        "You are an assistant that extracts the order_item_id or product name and the new return policy in days "
        "from user prompts. Respond with a JSON object like:\n"
        "{\"order_item_id\": \"CO-2750\", \"return_policy_days\": 55} or "
        "{\"name\": \"Incredible Concrete Chair\", \"return_policy_days\": 60}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        match = re.search(r'({.*})', content)
        if not match:
            return {"error": "Failed to parse response from OpenAI."}

        extracted = eval(match.group(1))  # Use `json.loads()` in production
        query = {}

        if "order_item_id" in extracted:
            query["order_item_id"] = extracted["order_item_id"]
        elif "name" in extracted:
            query["name"] = extracted["name"]
        else:
            return {"error": "No valid order_item_id or name provided."}

        item = collection.find_one(query)

        if not item:
            return {"error": "Item not found in database."}

        valid_days = extracted["return_policy_days"]
        policy_text = f"This item is returnable within {valid_days} days from the delivery date."

        update = {
            "$set": {
                "return_policy.valid_days": valid_days,
                "return_policy.policy_text": policy_text
            }
        }

        collection.update_one(query, update)

        return {
            "message": "Return policy updated successfully.",
            "updated_fields": {
                "valid_days": valid_days,
                "policy_text": policy_text
            }
        }

    except Exception as e:
        return {"error": str(e)}
