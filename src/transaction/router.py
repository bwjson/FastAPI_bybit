from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.base_config import is_authenticated
from src.auth.models import User
from src.database import get_async_session
from sqlalchemy import select, insert
from src.stock.models import Exchange
from src.wallet.models import Wallet
from src.transaction.repository import TransactionRepository
from src.transaction.schemas import TransactionCreate
from src.transaction.service import TransactionService
from src.transaction.dependencies import transaction_service

router = APIRouter(
	prefix="/api/transaction",
	tags=["Transaction"]
)

@router.post("/create")
async def create_transaction(
	new_transaction: TransactionCreate, 
	transaction_service: Annotated[TransactionService, Depends(transaction_service)],
	user: User = Depends(is_authenticated)
):
	try:
		response = await transaction_service.create_validated_transaction(new_transaction, user)
		return response
	except Exception as e:
		return HTTPException(
			status_code=400,
			detail=str(e)
		)
	
@router.get("/stakan-check")
async def stakan_check(
	transaction_service: Annotated[TransactionService, Depends(transaction_service)],
):
	try:
		await transaction_service.check_transaction_match()
		return {
			"status": "success"
		}
	except Exception as e:
		return HTTPException(
			status_code=400,
			detail=str(e)
		)
	



	
	
	

		
	

	
	
		
	



