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

	# query = select(Wallet).filter_by(user_id=user.id)
	# wallet_data = await session.execute(query)
	# has_wallet = wallet_data.scalar_one_or_none()

	# query = select(Exchange).filter_by(id=new_transaction.exchange_id)
	# exchange_data = await session.execute(query)
	# is_valid_exchange = exchange_data.scalar_one_or_none()


	# if has_wallet is None:
	# 	raise HTTPException(
	# 		status_code=400,
	# 		detail="you should create wallet first"
	# 	)
	
	# if is_valid_exchange is None:
	# 	raise HTTPException(
	# 		status_code=400,
	# 		detail="there is no such exchange id"
	# 	)
	
	

		
	

	
	
		
	



