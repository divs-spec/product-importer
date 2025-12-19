import uuid
from sqlalchemy import Column, String, Boolean, Text, Integer, DateTime, func, UniqueConstraint
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sku = Column(String, nullable=False)
    name = Column(String)
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    __table_args__ = (UniqueConstraint(func.lower(sku), name="uq_sku_lower"),)


class ImportJob(Base):
    __tablename__ = "import_jobs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="pending")
    processed = Column(Integer, default=0)
    total = Column(Integer, default=0)
    error = Column(Text)


class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String)
    event = Column(String)
    enabled = Column(Boolean, default=True)

