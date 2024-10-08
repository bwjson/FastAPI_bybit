from fastapi import HTTPException
from src.repository import AbstractRepository
from src.transaction.schemas import TransactionCreate
from src.transaction.repository import TransactionRepository

class TransactionService:
	def __init__(self, transaction_repo: TransactionRepository):
		self.transaction_repo = transaction_repo

	async def create_validated_transaction(self, new_transaction: TransactionCreate, user):
		if not await self.transaction_repo.wallet_exists(user.id):
			raise HTTPException(
				status_code=400,
				detail="You should create wallet first"
			)
		
		if not await self.transaction_repo.exchange_exists(new_transaction.exchange_id):
			raise HTTPException(
				status_code=400,
				detail="There is no such exchange with this ID"
			)
		
		transaction_dict = new_transaction.model_dump()

		await self.transaction_repo.create_one(transaction_dict)
		return {
			"status": "success",
			"new_transaction": new_transaction
		}


	

