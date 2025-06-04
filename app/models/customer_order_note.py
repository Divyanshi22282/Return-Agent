from datetime import datetime
from typing import Optional, Union
from beanie import Document, before_event, Insert, Replace
from pydantic import Field

class CustomerOrderNote(Document):
    order_notes_id:  Optional[Union[str, int]] = None
    customer_order_id:  Optional[Union[str, int]] = None
    customer_notes: Optional[Union[str, int]] = None
    merchant_notes:  Optional[Union[str, int]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)


    class Settings:
        name = "CustomerOrderNotes"
        
    