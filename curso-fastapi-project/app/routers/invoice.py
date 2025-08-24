from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Invoice
from db import SessionDep

router = APIRouter()

@router.post("/invoice", tags=["invoices"])
async def create_invoice(invoice_data: Invoice):
    return invoice_data