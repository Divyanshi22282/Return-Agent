import motor.motor_asyncio
from beanie import init_beanie
import asyncio
from decimal import Decimal
from app.models.customer_order_item import CustomerOrderItem
from app.models.order_fullfilment import OrderFulfillment
from app.models.custom_order import CustomerOrder, PaymentInfo, OrderItemInfo

from app.models.customer_order_history import CustomerOrderHistory
from  app.models.order_metadata import OrderMetadata
from app.models.order_payment import OrderPayment
from app.models.customer_order_note import CustomerOrderNote
from app.models.customer_order_audit import CustomerOrderAudit
from app.models.inventory_allocation import InventoryAllocation
from app.models.customer_order_address import CustomerOrderAddress
from app.models.sales_channel import SalesChannel
from app.models.inventory import InventoryRecord
from app.models.products import Product
MONGO_URI = "mongodb://dev-ekyam:MoPFOCdWDMByIMH@35.209.37.188:27018/?authSource=admin&directConnection=true"

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    db = client["ekyam_test_ai_agents_db"]
    collections = await db.list_collection_names()
    print("Collections in DB:", collections)

    await init_beanie(
        database=db,
        document_models=[
            CustomerOrderItem,
            OrderFulfillment,
            CustomerOrderAddress,
            CustomerOrderHistory,
            OrderMetadata,
            OrderPayment,
            CustomerOrderNote,
            CustomerOrderAudit,
            InventoryAllocation,
            CustomerOrder,
            SalesChannel,
            InventoryRecord,
            Product,
            
        ]
    )




     
    

    # children insert
    links_data = {
        "order_payment": []
    }
    data1 = [{
    "customer_order_id":"111",
    "order_payment_id":"123",
    
    

}]

    __docs= [OrderPayment(**item) for item in data1]
    response = await OrderPayment.insert_many(__docs)
    for ids in response.inserted_ids:
            links_data["order_payment"].append(str(ids))
    data = [
        {
            "customer_order_id": "123",
            "order_number": "1234",
            "customer_id": "gfgthyhy",
            "created_at": "2025-06-01T09:00:00Z",
            "updated_at": "2025-06-01T09:00:00Z",
            "status": "pending"
        }
    ]


    inserted_data = []
    print(links_data)
    for item in data:
        item["order_payment"] = []
        for link in links_data["order_payment"]:
            item["order_payment"].append(link)
        inserted_data.append(CustomerOrder(**item))
    print(inserted_data)
    response = await CustomerOrder.insert_many(inserted_data)   

if __name__ == "__main__":
    asyncio.run(init_db())