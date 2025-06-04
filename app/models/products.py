from typing import List, Dict, Optional, Any
from datetime import datetime, date
from pydantic import BaseModel
from beanie import Document, before_event, Insert, Replace
from pydantic import Field

class PricingTier(BaseModel):
    tier_id: str
    tier_name: str
    minimum_quantity: int
    price: str

class CurrencyPrice(BaseModel):
    currency: str
    amount: str

class AggregateStock(BaseModel):
    sales_channel_id: str
    sales_channel_name: str
    quantity: int

class Dimension(BaseModel):
    length: float
    width: float
    height: float

class Compliance(BaseModel):
    type: str
    description: str

class ExternalReference(BaseModel):
    system_short_code: str
    external_id: str

class Identifier(BaseModel):
    type: str
    value: str
    system: str

class Product(Document):
    product_id: str = Field(..., alias="_id")
    sku: str
    name: str
    brand_id: str
    manufacturer: str
    manufacturer_part_number: str
    warranty_period_days: Optional[int]
    warranty_terms: Optional[str]
    category_ids: List[str]
    category_names: List[str]
    category_slugs: List[str]
    collection_ids: List[str]
    partner_id: str
    attribute_set_id: str
    variant_ids: List[str]
    default_price: Dict[str, str]
    list_price: str
    sale_price: str
    cost_price: str
    profit_margin_percentage: float
    profit_margin_amount: str
    pricing_tiers: List[PricingTier]
    currency_prices: List[CurrencyPrice]
    aggregate_stock: List[AggregateStock]
    min_order_quantity: int
    max_order_quantity: int
    reorder_point: int
    reorder_quantity: int
    lead_time_days: int
    is_backorderable: bool
    weight: float
    product_dimensions: Dimension
    package_dimensions: Dimension
    tax_class: str
    pricing_tier: str
    discountable: bool
    compliances: List[Compliance]
    handling_instructions: List[str]
    meta_title: str
    meta_description: str
    meta_keywords: List[str]
    slug: str
    canonical_url: str
    release_date: Optional[date]
    discontinue_date: Optional[date]
    is_featured: bool
    is_active: bool
    is_available: bool
    external_references: List[ExternalReference]
    erp_id: str
    third_party_logistics_id: str
    crm_id: str
    cms_id: str
    payment_gateway_id: str
    marketing_platform_id: str
    identifiers: List[Identifier]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes_exist: bool

    class Settings:
        name = "Products"
        uid = "product_id"
