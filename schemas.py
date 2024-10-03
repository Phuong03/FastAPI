from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# Employee Schema
class EmployeeBase(BaseModel):
    name: str
    position: str
    store_id: int
    is_active: Optional[bool] = True

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    position: Optional[str]
    store_id: Optional[int]
    is_active: Optional[bool]

# Customer Schema
class CustomerBase(BaseModel):
    name: str
    email: str
    is_active: Optional[bool] = True

class CustomerUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]

# Admin Schema
class AdminBase(BaseModel):
    name: str
    email: str
    is_superadmin: Optional[bool] = False

class AdminUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]
    is_superadmin: Optional[bool]

# Store Schema
class StoreBase(BaseModel):
    name: str
    location: str

class StoreUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]

# Product Schema
class ProductBase(BaseModel):
    name: str
    price: float
    store_id: int

class ProductUpdate(BaseModel):
    name: Optional[str]
    price: Optional[float]
    store_id: Optional[int]

# Order Schema
class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderUpdate(BaseModel):
    customer_id: Optional[int]
    product_id: Optional[int]
    quantity: Optional[int]
    total_price: Optional[float]

# Invoice Schema
class InvoiceBase(BaseModel):
    order_id: int
    amount: float

class InvoiceUpdate(BaseModel):
    order_id: Optional[int]
    amount: Optional[float]

# Service Schema
class ServiceBase(BaseModel):
    name: str
    description: Optional[str] = None

class ServiceUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]

# Warranty Schema
class WarrantyBase(BaseModel):
    product_id: int
    service_id: int
    valid_until: datetime

class WarrantyUpdate(BaseModel):
    product_id: Optional[int]
    service_id: Optional[int]
    valid_until: Optional[datetime]
