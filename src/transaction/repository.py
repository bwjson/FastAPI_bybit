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