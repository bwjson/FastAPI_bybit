from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from src.auth.base_config import is_authenticated
from src.auth.models import User
from src.transaction.schemas import TransactionCreate, WalletTransactionCreate
from src.transaction.service import TransactionService
from src.transaction.dependencies import transaction_service
from src.transaction.utils import check_match
import asyncio

router = APIRouter(
    prefix="/api/transaction",
    tags=["transaction"]
)

@router.post("/create-order")
async def create_transaction(
    new_transaction: TransactionCreate,
    transaction_service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(is_authenticated)
):
    try:
        response = await transaction_service.create_transaction(new_transaction, user)
        return response
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/create-wallet")
async def create_wallet_transaction(
    new_transaction: WalletTransactionCreate,
    transaction_service: Annotated[TransactionService, Depends(transaction_service)],
    user: User = Depends(is_authenticated)
):
    try:
        response = await transaction_service.create_wallet_transaction(new_transaction, user)
        return response
    except Exception as e:
        return HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get("/order_book")
async def order_book_check():
    asyncio.create_task(check_match())
    return {"status": "Task started"}


















