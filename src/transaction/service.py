from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.repository import AbstractRepository
from src.transaction.schemas import TransactionCreate
from src.transaction.repository import TransactionRepository

# REFACTORING divide into validate data like exchange, ticker and is_payable part like here will be SELL, TOPUP, WITHDRAW, BUY

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
		
		if not await self.transaction_repo.ticker_exists(new_transaction.stock):
			raise HTTPException(
				status_code=400,
				detail="There is no such ticker"
			)
		
		if new_transaction.type == 'SELL':
			stocks = await self.transaction_repo.get_wallet_stocks_by_user(user.id)
			try:
				if stocks[new_transaction.stock] < new_transaction.amount:
					raise HTTPException(
					status_code=400,
					detail="You don't have needed amount of this ticker in your wallet"
				)
			except KeyError:
				raise HTTPException(
				status_code=400,
				detail="You don't have this ticker in your wallet"
			)

		elif new_transaction.type == 'BUY':
			user_balance = await self.transaction_repo.get_user_balance(user.id)
			if user_balance is None or user_balance < new_transaction.amount * new_transaction.price:
				raise HTTPException(
					status_code=400,
					detail="Your balance is lower than cost of transaction"
				)

		# elif new_transaction == 'TOPUP':
		# 	...

		# elif new_transaction == 'WITHDRAW':
		# 	...

		# else: 
		# 	raise HTTPException(
		# 		status_code=400,
		# 		detail="There is no such type of transaction"
		# 	)

		wallet_id = await self.transaction_repo.get_wallet_id(user.id)
		transaction_dict = new_transaction.model_dump()
		transaction_dict["wallet_id"] = wallet_id

		await self.transaction_repo.create_one(transaction_dict)
		return {
			"status": "success",
			"new_transaction": new_transaction
		}


	

