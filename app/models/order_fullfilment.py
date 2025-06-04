from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from beanie import Document, before_event, Insert, Replace
from pydantic import Field

class OrderFulfillment(Document):
    fulfillment_id: Optional[Union[str, int]] = None
    customer_order_id: Optional[Union[str, int]] = None
    warehouse_id: Optional[Union[str, int]] = None
    shipment_id: Optional[Union[str, int]] = None
    fulfillment_status: Optional[Union[str, int]] = None
    tracking_number: Optional[Union[str, int]] = None
    shipping_carrier: Optional[Union[str, int]] = None
    estimated_delivery: Optional[Union[str, int]] = None
    actual_delivery: Optional[Union[str, int]] = None
    
    fulfillment_notes: Optional[List[Dict[str, Any]]] =[]
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "OrderFullfillments"
        #uid = "fulfillment_id"

    
    