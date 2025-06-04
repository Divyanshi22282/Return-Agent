from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from datetime import datetime
from beanie import Document, Link, PydanticObjectId, before_event, Insert, Replace
from pydantic import Field, BaseModel

from app.models.inventory import InventoryRecord

class PricingDetails(BaseModel):
    discount: Optional[float]
    tax: Optional[float]
    currency: Optional[str]

class StatusFlags(BaseModel):
    is_bundle: Optional[bool] = False
    returnable: Optional[bool] = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class CustomerOrderItem(Document):
    order_item_id: Optional[Union[str, int]] = None
    customer_order_id: Optional[Union[str, int]] = None
    external_id: Optional[Union[str, int]] = None
    sku: Optional[Union[str, int]] = None
    product_id: Optional[Union[str, int]] = None
    name: Optional[Union[str, int]] = None
    quantity: Optional[Union[str, int]] = None
    price: Optional[Union[str, int,Decimal]] = None
    total_price: Optional[Union[str, int,Decimal]] = None
    status: Optional[Union[str, int]] = None
    description: Optional[Union[str, int]] = None
    category: Optional[Union[str, int]] = None
    image_url: Optional[Union[str, int]] = None
    vendor_id: Optional[Union[str, int]] = None
    pricing_details: Optional[PricingDetails] 
    status_flags: Optional[StatusFlags] = None
    return_policy:Optional[StatusFlags] =None
    inventory_reference: Optional[List[Link[InventoryRecord]]]
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "CustomerOrderItem"
       
    
    