from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from database import Base 
from sqlalchemy.orm import relationship
from datetime import datetime



# Customer Model
# Employee Model
class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    store_id = Column(Integer, ForeignKey("stores.id"))  # Relation with Store
    is_active = Column(Boolean, default=True)
    store = relationship("Store", back_populates="employees")

# Customer Model
class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="customer")

# Admin Model
class Admin(Base):
    __tablename__ = "admins"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_superadmin = Column(Boolean, default=False)

# Store Model
class Store(Base):
    __tablename__ = "stores"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    employees = relationship("Employee", back_populates="store")
    products = relationship("Product", back_populates="store")

# Product Model
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    store_id = Column(Integer, ForeignKey("stores.id"))
    orders = relationship("Order", back_populates="product")
    store = relationship("Store", back_populates="products")

# Order Model
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    total_price = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")

# Invoice Model
class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    amount = Column(Float)
    issued_date = Column(DateTime, default=datetime.utcnow)
    order = relationship("Order")

# Service Model
class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Warranty Model
class Warranty(Base):
    __tablename__ = "warranties"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    valid_until = Column(DateTime)
    product = relationship("Product")
    service = relationship("Service")