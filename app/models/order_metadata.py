from typing import Optional, Dict, Any, Union
from datetime import datetime
from decimal import Decimal
from beanie import Document, before_event, Insert, Replace
from pydantic import Field


class OrderMetadata(Document):
    order_metadata_id: Optional[Union[str, int]] = None
    customer_order_id: Optional[Union[str, int]] = None
    source_system: Optional[Union[str, int]] = None
    sales_channel_id: Optional[Union[str, int]] = None
    fraud_score: Optional[Union[str, int]] = None
    delivery_instructions: Optional[Union[str, int]] = None
    gift_message: Optional[Union[str, int]] = None
    is_gift: Optional[Union[str, int,bool]] = None
    tax_amount: Optional[Union[str, int, Decimal]] = None
    tax_details:Optional[Union[str, int]] = None
    rma_number: Optional[Union[str, int]] = None
    installment_plan_details: Optional[Union[str, int]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "OrderMetadata"
        #uid = "order_metadata_id"

    