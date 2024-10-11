from fastapi import HTTPException
from src.transaction.schemas import TransactionCreate
from src.transaction.repository import TransactionRepository


class TransactionService:
	def __init__(self, trans_repo: TransactionRepository):
		self.trans_repo = trans_repo

	async def create_validated_transaction(self, new_transaction: TransactionCreate, user):
		if not await self.trans_repo.wallet_exists(user.id):
			raise HTTPException(
				status_code=400,
				detail="You should create wallet first"
			)
		
		if not await self.trans_repo.exchange_exists(new_transaction.exchange_id):
			raise HTTPException(
				status_code=400,
				detail="There is no such exchange with this ID"
			)
		
		if not await self.trans_repo.ticker_exists(new_transaction.stock):
			raise HTTPException(
				status_code=400,
				detail="There is no such ticker"
			)
		
		if new_transaction.type == 'SELL':
			stocks = await self.trans_repo.get_wallet_stocks(user.id)

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
			user_balance = await self.trans_repo.get_user_balance(user.id)
			if user_balance is None or user_balance < new_transaction.amount * new_transaction.price:
				raise HTTPException(
					status_code=400,
					detail="Your balance is lower than cost of transaction"
				)
		
		wallet_id = await self.trans_repo.get_wallet_id(user.id)
		transaction_dict = new_transaction.model_dump()
		transaction_dict["wallet_id"] = wallet_id

		await self.trans_repo.create_one(transaction_dict)
		return {
			"status": "success",
			"new_transaction": new_transaction
		}

	async def check_transaction_match(self):
		sell_orders = await self.trans_repo.get_sell_orders()
		buy_orders = await self.trans_repo.get_buy_orders()

		for sell_order in sell_orders:
			for buy_order in buy_orders:
				if not sell_order.price <= buy_order.price:
					break
				if not sell_order.stock == buy_order.stock:
					break
				if not sell_order.exchange_id == buy_order.exchange_id:
					break
				if not sell_order.wallet_id != buy_order.wallet_id:
					break
				await self.execute_order(sell_order, buy_order)
				

	async def execute_order(self, buy_transaction, sell_transaction):
		await self.trans_repo.change_user_balance(buy_transaction.wallet_id, buy_transaction.amount, buy_transaction.price, buy_transaction.type)
		await self.trans_repo.change_user_balance(sell_transaction.wallet_id, sell_transaction.amount, sell_transaction.price, sell_transaction.type)
		await self.trans_repo.change_user_stocks(buy_transaction.wallet_id, buy_transaction.stock, buy_transaction.amount, buy_transaction.type)
		await self.trans_repo.change_user_stocks(sell_transaction.wallet_id, sell_transaction.stock, sell_transaction.amount, sell_transaction.type)
		await self.trans_repo.delete_one(buy_transaction.id)
		await self.trans_repo.delete_one(sell_transaction.id)


		# elif new_transaction == 'TOPUP':
		# 	...

		# elif new_transaction == 'WITHDRAW':
		# 	...

		# else: 
		# 	raise HTTPException(
		# 		status_code=400,
		# 		detail="There is no such type of transaction"
		# 	)
 
		


	

