from abc import ABC, abstractmethod
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete
from src.database import get_async_session, async_session_maker
from src.transaction.models import Transaction

class AbstractRepository(ABC):
	@abstractmethod
	async def create_one():
		raise NotImplementedError
	# @abstractmethod
	# async def get_all():
	# 	raise NotImplementedError
	# @abstractmethod
	# async def delete_one():
	# 	raise NotImplementedError

class SQLAlchemyRepository(AbstractRepository):
	model = None	

	async def create_one(self, data: dict) -> int:
		async with async_session_maker() as session:
			try:
				stmt = insert(self.model).values(data).returning(self.model.id)
				res = await session.execute(stmt)
				await session.commit()
				return res.scalar_one() 
			except SQLAlchemyError as e:
				await session.rollback()
				raise HTTPException(
					status_code=400,
					detail=str(e)
				)

	


		
		
	
