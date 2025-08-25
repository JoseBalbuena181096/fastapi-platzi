from fastapi import FastAPI, HTTPException, status
import zoneinfo
import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Transaction, Invoice
from db import SessionDep, create_all_tables
from sqlmodel import select
from .utils import country_timezones
from .routers import customer, transaction, invoice, plans
import time
from fastapi import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from fastapi import Depends


app = FastAPI(lifespan=create_all_tables)
app.include_router(customer.router)
app.include_router(transaction.router)
app.include_router(invoice.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    print(f"Request time: {request.url} completed in:  {end_time - start_time:.4f} seconds")
    return response
    
@app.middleware("http")
async def log_request_headers(request: Request, call_next):
    print("Request headers:")
    for header_name, header_value in request.headers.items():
        print(f"{header_name}: {header_value}")
    response = await call_next(request)
    return response


@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {
        "time": datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z (%z)")
    }
    
security = HTTPBasic()

@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username != "admin" or credentials.password != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"message": f"Hello {credentials.username}"}

