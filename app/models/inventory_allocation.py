from datetime import datetime
from typing import Literal, Optional, Union
from beanie import Document, before_event, Insert, Replace
from pydantic import Field

class InventoryAllocation(Document):
    inventory_allocation_id: Optional[Union[str, int]] = None
    sales_channel_id: Optional[Union[str, int]] = None
    product_id: Optional[Union[str, int]] = None
    inventory_id: Optional[Union[str, int]] = None
    allocated_quantity: Optional[Union[str, int]] = None
    reserved_quantity: Optional[Union[str, int]] = None
    available_quantity: Optional[Union[str, int]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "InventoryAllocation"
        #uid = "inventory_allocation_id"

    