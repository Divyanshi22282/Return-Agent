from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from beanie import Document, before_event, Insert, Replace
from pydantic import Field


class OrderPayment(Document):
    order_payment_id:  Optional[Union[str, int]] = None
    customer_order_id: Optional[Union[str, int]] = None
    transactions:Optional[Union[str, int]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    

    class Settings:
        name = "OrderPayment"
       # uid = "order_payment_id"

    