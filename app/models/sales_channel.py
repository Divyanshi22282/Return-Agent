from datetime import datetime
from typing import Optional, Literal
from beanie import Document, before_event, Insert, Replace
from pydantic import Field

class SalesChannel(Document):
    sales_channel_id: str = Field(..., alias="_id")
    name: str = Field(..., unique=True)
    description: Optional[str]
    channel_type: Literal["e-commerce", "marketplace", "retail", "B2B", "other"]
    status: Literal["active", "inactive"]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "SalesChannel"
        uid = "sales_channel_id"

    @before_event(Replace)
    def touch_updated_at(self):
        self.updated_at = datetime.utcnow()
