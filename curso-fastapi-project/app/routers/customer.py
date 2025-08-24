from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Customer, CustomerCreate, CustomerUpdate
from db import SessionDep
 
router = APIRouter()

@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()


@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer_db

@router.delete("/customers/{customer_id}", tags=["customers"])
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

@router.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED,
    tags=["customers"]
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

@router.get("/customers_mine/{customer_id}", response_model=Customer, tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    if customer := session.exec(select(Customer).where(Customer.id == customer_id)).first():
        return customer
    raise HTTPException(status_code=404, detail="Customer not found")


@router.put("/customers_mine/{customer_id}", response_model=Customer, tags=["customers"])
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
