from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from app.database.connection import init_db
from dateutil import parser
from datetime import datetime
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime, timedelta
from openai import OpenAI
import json
import uuid
from dotenv import load_dotenv
import os
import io
from PIL import Image
from PIL import ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import easypost
import requests

from app.models.customer_order_item import CustomerOrderItem

load_dotenv()

#  environment variables
easypost_api_key = os.getenv("EASYPOST_API_KEY")
fedex_api_key = os.getenv("FEDEX_API_KEY")
fedex_api_secret = os.getenv("FEDEX_API_SECRET")
fedex_account_number = os.getenv("FEDEX_ACCOUNT_NUMBER")
ryder_api_key = os.getenv("RYDER_API_KEY")
ryder_api_secret = os.getenv("RYDER_API_SECRET")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGODB_URI = os.getenv("MONGODB_URI")
client = OpenAI(api_key=OPENAI_API_KEY)

mongo = MongoClient(MONGODB_URI)
db = mongo["ekyam_test_ai_agents_db"]

collection = db["CustomerOrderItem"]

returns_col = db["returnorders"]
fulfill_col = db["OrderFullfillments"]
inventory_col =db['InventoryRecords']
address_col =db['CustomerOrdersAddress']


#label Generation has started.
client_easypost = easypost.EasyPostClient(easypost_api_key)

CARRIER_ACCOUNTS = {
    "FedEx": os.getenv("FEDEX_CARRIER_ID"),
    "UPS": os.getenv("UPS_CARRIER_ID"),
    "DHL Express": os.getenv("DHL_EXPRESS_CARRIER_ID"),
    "DHL eCommerce": os.getenv("DHL_ECOMMERCE_CARRIER_ID"),
    "USPS": os.getenv("USPS_CARRIER_ID"),
}

functions = [
    {
        "name": "parse_return_request",
        "description": "Extract return details from chat text",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {"type": "string", "description": "Customer order ID"},
                "product_name": {"type": "string", "description": "Product name"},
                "color": {"type": "string", "description": "Product color"},
                "reason": {"type": "string", "description": "Reason for return"}
            },
            "required": ["order_id", "product_name", "reason"]
        }
    }
]

class ChatInput(BaseModel):
    message: str

def validate_return(data):
    order_id = data["order_id"].strip()
    product_name = data["product_name"].strip()

    print("Validating return for Order ID:", order_id)
    print("Validating return for Product Name:", product_name)

    item = collection.find_one({
        "customer_order_id": order_id,
        "name": product_name
    })

    print("MongoDB query result:", item)

    if not item:
        return {"status": "error", "message": "Product not found in the given order."}

    if not item.get("status_flags", {}).get("returnable", True):
        return {"status": "denied", "message": "This product is marked as non-returnable."}
    return_policy = item.get("return_policy", {})
    valid_days = return_policy.get("valid_days")
    # 2. Lookup fulfillment to get actual_delivery and rec_updated_at
    fulfillment = fulfill_col.find_one({"customer_order_id": order_id})
    if not fulfillment:
        return {"status": "error", "message": "Fulfillment info not found for this order."}

    actual_delivery_raw = fulfillment.get("actual_delivery")

    if isinstance(actual_delivery_raw, datetime):
       delivered_date = actual_delivery_raw
    else:
        try:
           delivered_date = parser.parse(actual_delivery_raw)
        except Exception:
            return {
                "status": "error",
                "message": f"Invalid actual_delivery format: {actual_delivery_raw}"
            }
    # rec_updated_at is your “return-request timestamp”
    request_date = fulfillment.get("rec_updated_at")
    if not isinstance(request_date, datetime):
        # if stored as string, parse it
        try:
            request_date = datetime.fromisoformat(request_date)
        except Exception:
            return {"status": "error", "message": "Invalid rec_updated_at format in DB."}

    # 3. Check return window (30 days)
    if request_date - delivered_date > timedelta(days=valid_days):
        return {
            "status": "denied",
            "message": (
                f"Return window expired. Delivered on {delivered_date.date()}, "
                f"request made on {request_date.date()} (Return window was {valid_days} days)."
            )
        }
    # 4. Everything OK → generate RMA and persist
    carrier = fulfillment.get("shipping_carrier", "EasyPost")
    tracking_number = fulfillment.get("tracking_number", "")
    warehouse_id = fulfillment.get("warehouse_id", "")

    rma_number = str(uuid.uuid4()).upper()

    returns_col.insert_one({
        "rma_number": rma_number,
        "customer_order_id": order_id,
        "order_item_id": item.get("order_item_id"),
        "product_id": item.get("product_id"),
        "product_name": item.get("name"),
        "reason": data["reason"],
        "color": data.get("color"),
        "delivered_date": delivered_date.isoformat(),
        "request_date": request_date.isoformat(),
        "shipping_carrier": carrier,
        "tracking_number": tracking_number,
        "warehouse_id": warehouse_id,
        "created_at": datetime.utcnow().isoformat()
    })

    return {
        "status": "approved",
        "message": f"Return accepted—your RMA is {rma_number}.",
        "rma_number": rma_number,
        "shipping_carrier": carrier,
        "tracking_number": tracking_number,
        "warehouse_id": warehouse_id,
        "item": item
    }


async def return_request(chat: ChatInput):
    resp = client.chat.completions.create(
        model="gpt-4-0613",
        messages=[{"role":"user","content":chat.message}],
        functions=functions,
        function_call={"name":"parse_return_request"}
    )
    data = json.loads(resp.choices[0].message.function_call.arguments)
    result = validate_return(data)
    if result.get("status") != "approved":
        return JSONResponse(content={"parsed": data, "validation": result})

    order_id = data["order_id"]

    
    customer_order_items = await CustomerOrderItem.find(
        CustomerOrderItem.customer_order_id == order_id
    ).to_list()

    if not customer_order_items:
        raise HTTPException(status_code=404, detail="Customer order items not found.")

    warehouse_address = None
    for item in customer_order_items:
        await item.fetch_link("inventory_reference")  

        if item.inventory_reference:
            for inv_record in item.inventory_reference:
                warehouse_id = inv_record.warehouse_id
                inventory_warehouse = inventory_col.find_one({"warehouse_id": warehouse_id})
                if inventory_warehouse:
                    warehouse_address = inventory_warehouse
                    break
        if warehouse_address:
            break

    if not warehouse_address:
        raise HTTPException(status_code=500, detail="Warehouse address not found for linked inventory records.")
    
    fulfillment = fulfill_col.find_one({"customer_order_id": order_id})
    if not fulfillment:
        raise HTTPException(status_code=500, detail="Fulfillment info not found.")

    
    from_address = {
        "name": "Warehouse",
        "street1": warehouse_address.get("address_line_1"),
        "street2": warehouse_address.get("address_line_2"),
        "city": warehouse_address.get("city") or "San Francisco",
        "state": warehouse_address.get("state"),
        "zip": warehouse_address.get("postal_code"),
        "country": warehouse_address.get("country")
    }

    # Fetch customer address from CustomerOrdersAddress collection by order_id
    customer_address = address_col.find_one({"customer_order_id": order_id})
    if not customer_address:
        raise HTTPException(status_code=500, detail="Customer address not found.")

    # Format to_address for EasyPost
    to_address = {
        "name": "Customer",
        "street1": customer_address.get("street"),
        "street2": customer_address.get("address_line_2"),  # if you have this field, else remove
        "city": customer_address.get("city"),
        "state": customer_address.get("state"),
        "zip": customer_address.get("postal_code"),
        "country": customer_address.get("country")
    }

    shipping_carrier = fulfillment.get("shipping_carrier")
    if not shipping_carrier or shipping_carrier not in CARRIER_ACCOUNTS:
        raise HTTPException(status_code=400, detail=f"Unsupported or missing shipping carrier: {shipping_carrier}")

    carrier_account_id = CARRIER_ACCOUNTS[shipping_carrier]

    shipment = client_easypost.shipment.create(
        to_address=to_address,
        from_address=from_address,
        parcel={"length": 10, "width": 8, "height": 4, "weight": 16},
        carrier_accounts=[carrier_account_id],
        
        options={
        "reference": result["rma_number"],
        "label_format": "PDF"  # <- Ensure it's PDF
    }
    )
    bought = client_easypost.shipment.buy(shipment.id, rate=shipment.lowest_rate())
    print("Tracking number:", bought.tracking_code)
    fulfill_col.update_one(
        {"customer_order_id": order_id},
        {"$set": {"shipment_routed_to_warehouse": True, "warehouse_id": warehouse_address.get("warehouse_id")}}
    )

    resp = requests.get(bought.postage_label.label_url)
    resp.raise_for_status()  # Ensures download was successful

    return StreamingResponse(
    io.BytesIO(resp.content),
    media_type="application/pdf",
    headers={
        "Content-Disposition": f'attachment; filename="RMA_{result["rma_number"]}.pdf"',
        "X-RMA-Number": result["rma_number"],
        "X-Message": "The item is routed to its designated warehouse."
    },
)