from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from models import Transaction
from db import SessionDep
 
router = APIRouter()

@router.post("/transaction", tags=["transactions"])
async def create_transaction(transaction_data: Transaction):
    return transaction_data