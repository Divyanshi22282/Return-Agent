from datetime import datetime
from typing import Literal, Optional, Union
from beanie import Document, before_event, Insert, Replace,PydanticObjectId
from pydantic import Field


class CustomerOrderAddress(Document):
    order_address_id: Optional[Union[str, int]] = None
    customer_order_id:  Optional[Union[str, int]] = None
    address_type: Optional[Union[str, int]] = None
    street: Optional[Union[str, int]] = None
    city: Optional[Union[str, int]] = None
    state: Optional[Union[str, int]] = None
    postal_code: Optional[Union[str, int]] = None
    country: Optional[Union[str, int]] = None
    updated_at:  Optional[Union[str, int]] = None 
    created_at: Optional[Union[str, int]] = None 
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "CustomerOrdersAddress"
        #uid = "order_address_id"

    """@before_event(Insert)
    async def validate_insert(self):
        from app.models.custom_order import CustomerOrder
        order = await CustomerOrder.find_one(CustomerOrder.customer_order_id == self.customer_order_id)
        if not order:
            raise ValueError(f"Invalid customer_order_id: {self.customer_order_id} not found.")

    @before_event(Replace)
    def update_timestamp(self):
        self.updated_at = datetime.utcnow()"""