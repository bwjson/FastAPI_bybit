from fastapi import HTTPException
from src.transaction.schemas import TransactionCreate, WalletTransactionCreate
from src.transaction.repository import TransactionRepository


class TransactionService:
	def __init__(self, trans_repo: TransactionRepository):
		self.trans_repo = trans_repo

	async def create_validated_transaction(self, new_transaction: TransactionCreate, user):
		wallet_id = await self.trans_repo.get_wallet_id(user.id)

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
			blocked_stocks = await self.trans_repo.get_blocked_stocks(wallet_id, new_transaction.stock, new_transaction.exchange_id)
			current_stocks = stocks[new_transaction.stock]

			try:
				if stocks[new_transaction.stock] < new_transaction.amount:
					raise HTTPException(
					status_code=400,
					detail="You don't have needed amount of this ticker in your wallet"
				)
				if blocked_stocks + new_transaction.amount > current_stocks:
					raise HTTPException(
					status_code=400,
					detail=f"You have blocked stocks for other transactions: {blocked_stocks}; " \
						   f"Your available balance: {current_stocks - blocked_stocks}"
					)
			except KeyError:
				raise HTTPException(
				status_code=400,
				detail="You don't have this ticker in your wallet"
			)

		elif new_transaction.type == 'BUY':
			user_balance = await self.trans_repo.get_user_balance(user.id)
			blocked_funds = await self.trans_repo.get_blocked_funds(wallet_id, new_transaction.exchange_id)
			if user_balance is None or user_balance < new_transaction.amount * new_transaction.price:
				raise HTTPException(
					status_code=400,
					detail="Your balance is lower than cost of transaction"
				)
			if blocked_funds + new_transaction.amount * new_transaction.price > user_balance:
				raise HTTPException(
					status_code=400,
					detail=f"You have blocked balance for other transactions: {blocked_funds}; " \
						   f"Your available balance: {user_balance - blocked_funds}"
				)
		
		else: 
			raise HTTPException(
				status_code=400,
				detail="There is no such type of transaction"
			)
		
		transaction_dict = new_transaction.model_dump()
		transaction_dict["wallet_id"] = wallet_id

		await self.trans_repo.create_one(transaction_dict)
		return {
			"status": "success",
			"new_transaction": new_transaction
		}
	
	async def create_wallet_transaction(self, new_transaction: WalletTransactionCreate, user):
		wallet_id = await self.trans_repo.get_wallet_id(user.id)

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
		
		if new_transaction.type == 'TOPUP':
			current_balance = await self.trans_repo.get_user_balance(user.id)
			withdrawal_amount = new_transaction.deposit
			new_balance = current_balance + withdrawal_amount
			await self.trans_repo.change_wallet_balance(wallet_id, new_balance)

		elif new_transaction.type == 'WITHDRAW':
			current_balance = await self.trans_repo.get_user_balance(user.id)
			withdrawal_amount = new_transaction.deposit

			if withdrawal_amount > current_balance:
				raise HTTPException(
					status_code=400,
					detail=f"You are missing {withdrawal_amount - current_balance}, can not execute transaction"
				)
			
			new_balance = current_balance - withdrawal_amount
			await self.trans_repo.change_wallet_balance(wallet_id, new_balance)

		transaction_dict = new_transaction.model_dump()
		transaction_dict["wallet_id"] = wallet_id
		await self.trans_repo.create_one_wallet_transaction(transaction_dict)
		return {
			"status": "success",
			"new_transaction": new_transaction
		}

	async def check_transaction_match(self):
		print("check_transaction_match method called")
		sell_orders = await self.trans_repo.get_sell_orders()
		buy_orders = await self.trans_repo.get_buy_orders()

		for sell_order in sell_orders:
			for buy_order in buy_orders:
				if not sell_order.price <= buy_order.price:
					continue
				if not sell_order.stock == buy_order.stock:
					continue
				if not sell_order.exchange_id == buy_order.exchange_id:
					continue
				if not sell_order.wallet_id != buy_order.wallet_id:
					continue
				await self.execute_order(sell_order, buy_order)
				return		

	async def execute_order(self, buy_transaction, sell_transaction):
		order_price = min(buy_transaction.price, sell_transaction.price)
		order_amount = min(buy_transaction.amount, sell_transaction.amount)

		await self.trans_repo.change_user_balance(buy_transaction.wallet_id, order_amount, order_price, buy_transaction.type)
		await self.trans_repo.change_user_balance(sell_transaction.wallet_id, order_amount, order_price, sell_transaction.type)
		await self.trans_repo.change_user_stocks(buy_transaction.wallet_id, buy_transaction.stock, order_amount, buy_transaction.type)
		await self.trans_repo.change_user_stocks(sell_transaction.wallet_id, sell_transaction.stock, order_amount, sell_transaction.type)
		await self.trans_repo.delete_one(buy_transaction.id)
		await self.trans_repo.delete_one(sell_transaction.id)

 
		


	

