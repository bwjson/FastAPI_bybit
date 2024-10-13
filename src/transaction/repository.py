from src.repository import SQLAlchemyRepository
from src.transaction.models import Transaction, WalletTransaction
from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete, update, values, func
from src.database import get_async_session, async_session_maker
from src.transaction.models import Transaction
from src.wallet.models import Wallet
from src.stock.models import Stock
from src.exchange.models import Exchange
from src.stock.utils import KaseAPIClient
import json

class TransactionRepository(SQLAlchemyRepository):
	model = Transaction

	async def wallet_exists(self, cur_user_id: int) -> bool:
		async with async_session_maker() as session:
			try:
				query = select(Wallet).filter_by(user_id=cur_user_id)
				res = await session.execute(query)
				return True if res.scalar_one_or_none() is not None else False 
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
					
	async def ticker_exists(self, ticker: str) -> bool:
		if KaseAPIClient.is_valid_ticker(ticker):
			return True
		return False
	
	async def get_wallet_stocks(self, cur_user_id: int):
		async with async_session_maker() as session:
			try:
				query = select(Wallet.stocks).filter_by(user_id=cur_user_id)
				response = await session.execute(query)
				stocks = response.scalar_one_or_none()
				return stocks
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
			
	async def get_sell_orders(self):
		async with async_session_maker() as session:
			try:
				query = select(Transaction).filter_by(type='SELL').order_by(Transaction.price)
				response = await session.execute(query)			
				sell_orders = list(response.scalars().all())
				return sell_orders
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				) 
			
	async def get_buy_orders(self):
		async with async_session_maker() as session:
			try:
				query = select(Transaction).filter_by(type='BUY').order_by(Transaction.price)
				response = await session.execute(query)
				buy_orders = list(response.scalars().all())
				return buy_orders
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
			
	async def get_wallet_id(self, cur_user_id: int) -> int:
		async with async_session_maker() as session:
			try:
				query = select(Wallet.id).filter_by(user_id=cur_user_id)
				response = await session.execute(query)
				res = response.scalar_one_or_none()

				if res is None:
					raise ValueError("There is no wallet with this ID") 
				return res
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
			
	async def get_user_balance(self, cur_user_id: int):
		async with async_session_maker() as session:
			try:
				query = select(Wallet.balance).filter_by(user_id=cur_user_id)
				response = await session.execute(query)
				user_balance = response.scalar_one_or_none()
				return user_balance
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
			
	async def change_user_balance(self, wallet_id: int, amount: int, price: int, transaction_type: str):
		async with async_session_maker() as session:
			query = select(Wallet.user_id).filter_by(id=wallet_id)
			response = await session.execute(query)
			cur_user_id = response.scalar_one_or_none()

			current_balance = await self.get_user_balance(cur_user_id)
			transaction_cost = amount * price
			
			if transaction_type == 'SELL':
				new_balance = current_balance + transaction_cost
				stmt = update(Wallet).filter_by(user_id=cur_user_id).values(balance=new_balance)
				await session.execute(stmt)
				await session.commit()
			elif transaction_type == 'BUY':
				new_balance = current_balance - transaction_cost
				stmt = update(Wallet).filter_by(user_id=cur_user_id).values(balance=new_balance)
				await session.execute(stmt)
				await session.commit()
	
	async def change_user_stocks(self, wallet_id: int, stock: str, amount: int, transaction_type: str):
		async with async_session_maker() as session:
			query = select(Wallet.user_id).filter_by(id=wallet_id)
			response = await session.execute(query)
			cur_user_id = response.scalar_one_or_none()
			current_stocks = await self.get_wallet_stocks(cur_user_id)

			if isinstance(current_stocks, str):
				current_stocks = json.loads(current_stocks)

			if transaction_type == 'SELL':
				current_amount = current_stocks.get(stock, 0)
				new_amount = current_amount - amount
				current_stocks[f'{stock}'] = new_amount

			elif transaction_type == 'BUY':
				current_amount = current_stocks.get(stock, 0)
				new_amount = current_amount + amount
				current_stocks[f'{stock}'] = new_amount

			stmt = update(Wallet).filter_by(user_id=cur_user_id).values(stocks=current_stocks)
			await session.execute(stmt)
			await session.commit()
			return {
				"status": "success"
			}

	async def get_blocked_funds(self, wallet_id: int, exchange_id: int) -> int:
		async with async_session_maker() as session:
			try:
				query = select(func.sum(Transaction.amount * Transaction.price)).filter_by(wallet_id=wallet_id, exchange_id=exchange_id)
				response = await session.execute(query)	
				blocked_funds = response.scalar_one_or_none()

				if blocked_funds is None:
					return 0
				return blocked_funds
			
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
				
	async def get_blocked_stocks(self, wallet_id: int, stock: str, exchange_id: int) -> int:
		async with async_session_maker() as session:
			try:
				query = select(func.sum(Transaction.amount)).filter_by(wallet_id=wallet_id, stock=stock, exchange_id=exchange_id)
				response = await session.execute(query)
				blocked_stocks = response.scalar_one_or_none()
				print(blocked_stocks)

				if blocked_stocks is None:
					return 0
				return blocked_stocks
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
			
	async def change_wallet_balance(self, wallet_id, new_balance):
		async with async_session_maker() as session:
			try:
				stmt = update(Wallet).filter_by(id=wallet_id).values(balance=new_balance).returning(Wallet.id)
				response = await session.execute(stmt)
				await session.commit()

				if response is None:
					raise HTTPException(status_code=404, detail="Wallet ID not found.")
				return {
					"wallet_id": wallet_id
				}
			except SQLAlchemyError as e:
				await session.rollback()
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)

	async def create_one_wallet_transaction(self, data: dict) -> int:
		async with async_session_maker() as session:
			try:
				stmt = insert(WalletTransaction).values(data).returning(WalletTransaction.id)
				res = await session.execute(stmt)
				await session.commit()
				return res.scalar_one() 
			except SQLAlchemyError as e:
				await session.rollback()
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)

	 