from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from decimal import Decimal
from beanie import Document, Link, before_event, Insert, Replace,PydanticObjectId

from pydantic import Field
from pydantic import BaseModel
from typing import Literal
from bson.decimal128 import Decimal128

from app.models.customer_order_address import CustomerOrderAddress
from app.models.customer_order_audit import CustomerOrderAudit
from app.models.customer_order_history import CustomerOrderHistory
from app.models.customer_order_item import CustomerOrderItem
from app.models.customer_order_note import CustomerOrderNote
from app.models.inventory import InventoryRecord
from app.models.inventory_allocation import InventoryAllocation
from app.models.order_fullfilment import OrderFulfillment
from app.models.order_metadata import OrderMetadata
from app.models.order_payment import OrderPayment
from app.models.products import Product
class PaymentInfo(BaseModel):
    method: Optional[Union[str, int]] = None
    status: Optional[Union[str, int]] = None
    amount_paid: Optional[Union[str, int,Decimal]] = None
    

class OrderItemInfo(BaseModel):
    product_id: Optional[Union[str, int]] = None
    name: Optional[Union[str, int]] = None
    quantity: Optional[Union[str, int, Decimal]] = None
    unit_price: Optional[Union[str, int, Decimal]] = None
    total_price: Optional[Union[str, int,Decimal]] = None
    

class CustomerOrder(Document):
    customer_order_id: Optional[Union[str, int]] = None 
    order_number: Optional[Union[str, int]] = None
    customer_id:  Optional[Union[str, int]] = None
    order_type: Optional[Union[str, int]] = None
    created_at: Optional[Union[str, int]] = None
    updated_at: Optional[Union[str, int]] = None
    status:Optional[Union[str, int]] = None
    total_amount: Optional[Union[str, int,float]] = None
    payment: Optional[Union[str, int,float]] = None
    is_multi_address: Optional[Union[str,bool]] = None
    shipping_address_id: Optional[Union[str, int]] = None
    items: Optional[List[OrderItemInfo]] = []
    promotions: Optional[List[Dict[str, Any]]]=[]
    order_notes_exist: Optional[Union[str, int, bool]] = None
    additional_info: Optional[Dict[str, Any]]=[]
    fulfillment_id: Optional[str]=None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)
    updated_at:  Optional[Union[str, int]] = None 
    created_at: Optional[Union[str, int]] = None 
    customer_order_address: Optional[List[Link[CustomerOrderAddress]]] = []
    customer_order_audit: Optional[List[Link[CustomerOrderAudit]]] = []
    customer_order_history: Optional[List[Link[CustomerOrderHistory]]] = []
    customer_order_item: Optional[List[Link[CustomerOrderItem]]] = []
    customer_order_note: Optional[List[Link[CustomerOrderNote]]] = []
    customer_inventory: Optional[list[Link[InventoryAllocation]]] =[]
    inventory_record:Optional[list[Link[InventoryRecord]]] =[]
    order_fullfilment:Optional[list[Link[OrderFulfillment]]] =[]
    order_metadata:Optional[List[Link[OrderMetadata]]]=[]
    order_payment:Optional[List[Link[OrderPayment]]]=[]
    products:Optional[List[Link[Product]]]=[]

    class Settings:
        name = "CustomerOrder"
        #uid = "customer_order_id"
 