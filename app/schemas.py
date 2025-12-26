from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------- Products ----------

class ProductBase(BaseModel):
    sku: str
    name: Optional[str] = None
    description: Optional[str] = None
    active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    active: Optional[bool]

class ProductOut(ProductBase):
    id: str
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------- Import Jobs ----------

class ImportJobOut(BaseModel):
    id: str
    status: str
    processed: int
    total: int
    error: Optional[str]

    class Config:
        from_attributes = True


# ---------- Webhooks ----------

class WebhookCreate(BaseModel):
    url: str
    event: str
    enabled: bool = True

class WebhookOut(WebhookCreate):
    id: str

    class Config:
        from_attributes = True

