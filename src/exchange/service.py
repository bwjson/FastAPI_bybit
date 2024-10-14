from fastapi import HTTPException
from src.exchange.schemas import ExchangeCreate
from src.exchange.repository import ExchangeRepository


class ExchangeService:
	def __init__(self, exc_repo: ExchangeRepository):
		self.exc_repo = exc_repo

	async def create_one_stock(self, new_exc: ExchangeCreate):
		new_exc_dict = new_exc.model_dump()

		if await self.exc_repo.create_one(new_exc_dict) is None:
			return {
				"status": "Failed creating the instance",
			}
		return {
			"status": "Successfully added the instance"
		}
	
	async def delete_one_stock(self, id):
		if await self.exc_repo.delete_one(id) is None:
			return {
				"status": "Failed deleting the instance"
			}
		return {
			"status": "Record deleted successfully", 
			"updated_id": id
		}
	