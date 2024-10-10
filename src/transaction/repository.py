from fastapi.responses import JSONResponse
from src.repository import SQLAlchemyRepository
from src.transaction.models import Transaction
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete
from src.database import get_async_session, async_session_maker
from src.transaction.models import Transaction
from src.wallet.models import Wallet
from src.stock.models import *
from src.stock.utils import is_valid_ticker

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
			
	async def exchange_exists(self, cur_exchange_id: int) -> bool:
		async with async_session_maker() as session:
			try:
				query = select(Exchange).filter_by(id=cur_exchange_id)
				res = await session.execute(query)
				return True if res.scalar_one_or_none() is not None else False
			except SQLAlchemyError as e:
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)
	
	async def ticker_exists(self, ticker: str) -> bool:
		if is_valid_ticker(ticker):
			return True
		return False
			
	async def get_wallet_id(self, cur_user_id: int) -> int:
		async with async_session_maker() as session:
			try:
				query = select(Wallet.id).filter_by(user_id=cur_user_id)
				response = await session.execute(query)
				res = response.scalar_one_or_none()
				print(res)

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

	async def get_wallet_stocks_by_user(self, cur_user_id: int) -> dict:
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
			