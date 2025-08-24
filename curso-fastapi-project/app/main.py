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

app = FastAPI(lifespan=create_all_tables)
app.include_router(customer.router)
app.include_router(transaction.router)
app.include_router(invoice.router)
app.include_router(plans.router)

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




