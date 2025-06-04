from datetime import datetime
from typing import Optional, Dict, Any, Union
from beanie import Document, before_event, Insert, Replace, PydanticObjectId
from pydantic import Field


class CustomerOrderAudit(Document):
    audit_id:  Optional[Union[str, int]] = None
    entity_name: Optional[Union[str, int]] = None
    entity_id: Optional[Union[str, int]] = None
    action: Optional[Union[str, int]] = None
    performed_by: Optional[Union[str, int]] = None
    change_type: Optional[Union[str, int]] = None
    changes: Optional[Union[str, int]] = None
    source_system: Optional[Union[str, int]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "CustomerOrderAudit"
        #uid = "audit_id"

    '''@before_event(Insert)
    async def validate_customer_order(self):
     if self.entity_name == "CustomerOrder":
        from app.models.custom_order import CustomerOrder
        if not await CustomerOrder.get(self.entity_id):
            raise ValueError(f"Invalid entity_id for CustomerOrder: {self.entity_id} not found.")
    @before_event(Replace)
    def touch_timestamp(self):
        self.timestamp = datetime.utcnow()'''
