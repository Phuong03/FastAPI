from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Annotated, Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from typing import List, Annotated
import models 
import schemas




# FastAPI application instance
app = FastAPI()
models.Base.metadata.create_all(bind=engine)



# Dependency để lấy session của DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD cho Employees
@app.post("/employees/", response_model=schemas.EmployeeBase)
async def create_employee(employee: schemas.EmployeeBase, db: Session = Depends(get_db)):
    db_employee = models.Employee(name=employee.name, position=employee.position, store_id=employee.store_id)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/{employee_id}", response_model=schemas.EmployeeBase)
async def read_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.put("/employees/{employee_id}", response_model=schemas.EmployeeBase)
async def update_employee(employee_id: int, employee_update: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for var, value in vars(employee_update).items():
        if value or value is not None:
            setattr(employee, var, value)
    
    db.commit()
    db.refresh(employee)
    return employee

@app.delete("/employees/{employee_id}", response_model=dict)
async def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(employee)
    db.commit()
    return {"detail": "Employee deleted successfully"}

# CRUD cho Customers 
@app.post("/customers/", response_model=schemas.CustomerBase)
async def create_customer(customer: schemas.CustomerBase, db: Session = Depends(get_db)):
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=schemas.CustomerBase)
async def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}", response_model=schemas.CustomerBase)
async def update_customer(customer_id: int, customer_update: schemas.CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for var, value in vars(customer_update).items():
        if value or value is not None:
            setattr(customer, var, value)
    
    db.commit()
    db.refresh(customer)
    return customer

@app.delete("/customers/{customer_id}", response_model=dict)
async def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(customer)
    db.commit()
    return {"detail": "Customer deleted successfully"}

# CRUD cho Store
# POST: Tạo một Store mới
@app.post("/stores/", response_model=schemas.StoreBase)
async def create_store(store: schemas.StoreBase, db: Session = Depends(get_db)):
    db_store = models.Store(name=store.name, location=store.location)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

# GET: Lấy thông tin một Store
@app.get("/stores/{store_id}", response_model=schemas.StoreBase)
async def read_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store

# PUT: Cập nhật thông tin một Store
@app.put("/stores/{store_id}", response_model=schemas.StoreBase)
async def update_store(store_id: int, store_update: schemas.StoreUpdate, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    for var, value in vars(store_update).items():
        if value or value is not None:
            setattr(store, var, value)
    
    db.commit()
    db.refresh(store)
    return store

# DELETE: Xóa một Store
@app.delete("/stores/{store_id}", response_model=dict)
async def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.id == store_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    
    db.delete(store)
    db.commit()
    return {"detail": "Store deleted successfully"}

# CRUD cho Product
# POST: Tạo một Product mới
@app.post("/products/", response_model=schemas.ProductBase)
async def create_product(product: schemas.ProductBase, db: Session = Depends(get_db)):
    db_product = models.Product(name=product.name, price=product.price, store_id=product.store_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# GET: Lấy thông tin một Product
@app.get("/products/{product_id}", response_model=schemas.ProductBase)
async def read_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# PUT: Cập nhật thông tin một Product
@app.put("/products/{product_id}", response_model=schemas.ProductBase)
async def update_product(product_id: int, product_update: schemas.ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for var, value in vars(product_update).items():
        if value or value is not None:
            setattr(product, var, value)
    
    db.commit()
    db.refresh(product)
    return product

# DELETE: Xóa một Product
@app.delete("/products/{product_id}", response_model=dict)
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"detail": "Product deleted successfully"}

# CRUD cho Order
# POST: Tạo một Order mới
@app.post("/orders/", response_model=schemas.OrderBase)
async def create_order(order: schemas.OrderBase, db: Session = Depends(get_db)):
    db_order = models.Order(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=order.total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# GET: Lấy thông tin một Order
@app.get("/orders/{order_id}", response_model=schemas.OrderBase)
async def read_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# PUT: Cập nhật thông tin một Order
@app.put("/orders/{order_id}", response_model=schemas.OrderBase)
async def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    for var, value in vars(order_update).items():
        if value or value is not None:
            setattr(order, var, value)
    
    db.commit()
    db.refresh(order)
    return order

# DELETE: Xóa một Order
@app.delete("/orders/{order_id}", response_model=dict)
async def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return {"detail": "Order deleted successfully"}


# CRUD cho Invoice
# POST: Tạo một Invoice mới
@app.post("/invoices/", response_model=schemas.InvoiceBase)
async def create_invoice(invoice: schemas.InvoiceBase, db: Session = Depends(get_db)):
    db_invoice = models.Invoice(order_id=invoice.order_id, amount=invoice.amount)
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

# GET: Lấy thông tin một Invoice
@app.get("/invoices/{invoice_id}", response_model=schemas.InvoiceBase)
async def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

# PUT: Cập nhật thông tin một Invoice
@app.put("/invoices/{invoice_id}", response_model=schemas.InvoiceBase)
async def update_invoice(invoice_id: int, invoice_update: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    for var, value in vars(invoice_update).items():
        if value or value is not None:
            setattr(invoice, var, value)
    
    db.commit()
    db.refresh(invoice)
    return invoice

# DELETE: Xóa một Invoice
@app.delete("/invoices/{invoice_id}", response_model=dict)
async def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    db.delete(invoice)
    db.commit()
    return {"detail": "Invoice deleted successfully"}


# POST: Tạo một Service mới
@app.post("/services/", response_model=schemas.ServiceBase)
async def create_service(service: schemas.ServiceBase, db: Session = Depends(get_db)):
    db_service = models.Service(name=service.name, description=service.description)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

# GET: Lấy thông tin một Service
@app.get("/services/{service_id}", response_model=schemas.ServiceBase)
async def read_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

# PUT: Cập nhật thông tin một Service
@app.put("/services/{service_id}", response_model=schemas.ServiceBase)
async def update_service(service_id: int, service_update: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    for var, value in vars(service_update).items():
        if value or value is not None:
            setattr(service, var, value)
    
    db.commit()
    db.refresh(service)
    return service

# DELETE: Xóa một Service
@app.delete("/services/{service_id}", response_model=dict)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(service)
    db.commit()
    return {"detail": "Service deleted successfully"}


# CRUD cho Service
# POST: Tạo một Service mới
@app.post("/services/", response_model=schemas.ServiceBase)
async def create_service(service: schemas.ServiceBase, db: Session = Depends(get_db)):
    db_service = models.Service(name=service.name, description=service.description)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

# GET: Lấy thông tin một Service
@app.get("/services/{service_id}", response_model=schemas.ServiceBase)
async def read_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

# PUT: Cập nhật thông tin một Service
@app.put("/services/{service_id}", response_model=schemas.ServiceBase)
async def update_service(service_id: int, service_update: schemas.ServiceUpdate, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    for var, value in vars(service_update).items():
        if value or value is not None:
            setattr(service, var, value)
    
    db.commit()
    db.refresh(service)
    return service

# DELETE: Xóa một Service
@app.delete("/services/{service_id}", response_model=dict)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(models.Service).filter(models.Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(service)
    db.commit()
    return {"detail": "Service deleted successfully"}


# CRUD cho Warranty
# POST: Tạo một Warranty mới
@app.post("/warranties/", response_model=schemas.WarrantyBase)
async def create_warranty(warranty: schemas.WarrantyBase, db: Session = Depends(get_db)):
    db_warranty = models.Warranty(product_id=warranty.product_id, warranty_period=warranty.warranty_period)
    db.add(db_warranty)
    db.commit()
    db.refresh(db_warranty)
    return db_warranty

# GET: Lấy thông tin một Warranty
@app.get("/warranties/{warranty_id}", response_model=schemas.WarrantyBase)
async def read_warranty(warranty_id: int, db: Session = Depends(get_db)):
    warranty = db.query(models.Warranty).filter(models.Warranty.id == warranty_id).first()
    if not warranty:
        raise HTTPException(status_code=404, detail="Warranty not found")
    return warranty

# PUT: Cập nhật thông tin một Warranty
@app.put("/warranties/{warranty_id}", response_model=schemas.WarrantyBase)
async def update_warranty(warranty_id: int, warranty_update: schemas.WarrantyUpdate, db: Session = Depends(get_db)):
    warranty = db.query(models.Warranty).filter(models.Warranty.id == warranty_id).first()
    if not warranty:
        raise HTTPException(status_code=404, detail="Warranty not found")
    
    for var, value in vars(warranty_update).items():
        if value or value is not None:
            setattr(warranty, var, value)
    
    db.commit()
    db.refresh(warranty)
    return warranty

# DELETE: Xóa một Warranty
@app.delete("/warranties/{warranty_id}", response_model=dict)
async def delete_warranty(warranty_id: int, db: Session = Depends(get_db)):
    warranty = db.query(models.Warranty).filter(models.Warranty.id == warranty_id).first()
    if not warranty:
        raise HTTPException(status_code=404, detail="Warranty not found")
    
    db.delete(warranty)
    db.commit()
    return {"detail": "Warranty deleted successfully"}




