from fastapi import FastAPI, HTTPException, status
import zoneinfo
import datetime
from models import Customer, Transaction, Invoice, CustomerCreate, CustomerUpdate
from db import SessionDep, create_all_tables
from sqlmodel import select
from utils import country_timezones

app = FastAPI(lifespan=create_all_tables)

@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {
        "time": datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z (%z)")
    }
    

@app.get("/")
async def root():
    return {"message": "Hello World from Jose"}

@app.post("/customers", response_model=Customer)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db

@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    # eliminar un elemento
    session.delete(customer_db)
    session.commit()
    return {
        "detail": "Customer deleted"
    }

@app.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED
)
async def patch_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    # actualizar solo los campos que se hayan enviado
    cusomer_data_dict = customer_data.model_dump(exclude_unset=True)
    # creamos la querie para actualizar
    customer_db.sqlmodel_update(cusomer_data_dict)
    # añadimos la query
    session.add(customer_db)
    # ejecutamos la query
    session.commit()
    # actualizamos el objeto con los datos de la base de datos
    session.refresh(customer_db)
    return customer_db

@app.get("/customers_mine/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int, session: SessionDep):
    if customer := session.exec(select(Customer).where(Customer.id == customer_id)).first():
        return customer
    raise HTTPException(status_code=404, detail="Customer not found")


@app.put("/customers_mine/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer_data: CustomerCreate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    customer_db.name = customer_data.name
    customer_db.description = customer_data.description
    customer_db.email = customer_data.email
    customer_db.age = customer_data.age
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db


@app.post("/transaction")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoice")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

