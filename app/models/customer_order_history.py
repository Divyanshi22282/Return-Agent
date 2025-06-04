from datetime import datetime
from typing import Optional, Union
from beanie import Document, before_event, Insert, Replace
from pydantic import Field

class CustomerOrderHistory(Document):
    order_status_history_id: Optional[Union[str, int]] = None
    customer_order_id: Optional[Union[str, int]] = None
    previous_status: Optional[Union[str, int]] = None
    new_status:Optional[Union[str, int]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "CustomerOrderHistory"
        
