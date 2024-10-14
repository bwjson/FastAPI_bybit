from abc import ABC, abstractmethod
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, select, delete, update
from src.database import async_session_maker
from src.exchange.models import Exchange
from src.wallet.models import Wallet

class AbstractRepository(ABC):
	@abstractmethod
	async def create_one(self, data: dict) -> int:
		raise NotImplementedError
	
	@abstractmethod
	async def delete_one(self, id: int) -> dict:
		raise NotImplementedError
	
	@abstractmethod
	async def update_one(self, id: int, field: str, new_value: str) -> dict:
		raise NotImplementedError
	
	@abstractmethod
	async def get_all(self) -> list:
		raise NotImplementedError
	
	@abstractmethod
	async def get_one(self, id: int) -> dict:
		raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
	model = None

	async def create_one(self, data: dict) -> int:
		async with async_session_maker() as session:
			try:
				stmt = insert(self.model).values(data).returning(self.model.id)
				res = await session.execute(stmt)
				await session.commit()
				return res.scalar_one_or_none()
			except SQLAlchemyError as e:
				await session.rollback()
				raise HTTPException(status_code=400, detail=str(e))

	async def delete_one(self, id: int) -> dict:
		async with async_session_maker() as session:
			try:
				stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
				res = await session.execute(stmt)
				await session.commit()
				response = res.scalar_one_or_none()
				return response
			except SQLAlchemyError as e:
				await session.rollback()
				raise HTTPException(status_code=400, detail=str(e))

	async def update_one(self, id: int, field: str, new_value: str) -> dict:
		async with async_session_maker() as session:
			try:
				stmt = (
					update(self.model)
					.where(self.model.id == id)
					.values({getattr(self.model, field): new_value})
					.returning(self.model.id)
					.execution_options(synchronize_session="fetch")
				)
				response = await session.execute(stmt)
				await session.commit()
				updated_id = response.scalar_one_or_none()
				return updated_id
			except SQLAlchemyError as e:
				await session.rollback()
				raise HTTPException(status_code=400, detail=str(e))

	async def get_all(self) -> list:
		async with async_session_maker() as session:
			try:
				stmt = select(self.model)
				res = await session.execute(stmt)
				results = res.scalars().all()
				return results
			except SQLAlchemyError as e:
				raise HTTPException(status_code=400, detail=str(e))

	async def get_one(self, id: int) -> dict:
		async with async_session_maker() as session:
			try:
				stmt = select(self.model).where(self.model.id == id)
				res = await session.execute(stmt)
				result = res.scalar_one_or_none()
				return result
			except SQLAlchemyError as e:
				raise HTTPException(status_code=400, detail=str(e))
				
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