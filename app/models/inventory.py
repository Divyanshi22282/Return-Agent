from typing import List, Dict, Optional, Any, Union
from datetime import datetime, date
from pydantic import BaseModel
from beanie import Document, before_event, Insert, Replace
from pydantic import Field
# InventoryRecord model
class InventoryRecord(Document):
    inventory_id: Optional[Union[str, int]] = None
    warehouse_id: Optional[Union[str, int]] = None
    variant_id: Optional[Union[str, int]] = None
    sku: Optional[Union[str, int]] = None
    location_id: Optional[Union[str, int]] = None
    quantity: Optional[Union[str, int]] = None
    reserved: Optional[Union[str, int]] = None
    available: Optional[Union[str, int]] = None
    reorder_point: Optional[Union[str, int]] = None
    reorder_quantity: Optional[Union[str, int]] = None
    lead_time_days: Optional[Union[str, int]] = None
    erp_id: Optional[Union[str, int]] = None
    third_party_logistics_id: Optional[Union[str, int]] = None
    crm_id: Optional[Union[str, int]] = None
    cms_id: Optional[Union[str, int]] = None
    payment_gateway_id: Optional[Union[str, int]] = None
    marketing_platform_id: Optional[Union[str, int]] = None
    address_line_1: Optional[Union[str, int]] = None
    address_line_2: Optional[Union[str, int]] = None
    state: Optional[Union[str, int]] = None
    postal_code: Optional[Union[str, int]] = None
    country: Optional[Union[str, int]] = None
    latitude: Optional[Union[str, int, float]] = None
    longitude: Optional[Union[str, int,float]] = None
    city: Optional[Union[str, int]] = None
    phone: Optional[Union[str, int,float]] = None
    rec_created_at: datetime = Field(default_factory=datetime.now)
    rec_updated_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "InventoryRecords"
        #uid = "inventory_id"

    