from fastapi import HTTPException
from src.stock.schemas import StockCreate
from src.stock.repository import StockRepository
from src.stock.utils import KaseAPIClient


class StockService:
	def __init__(self, stock_repo: StockRepository):
		self.stock_repo = stock_repo

	async def create_one_stock(self, new_stock: StockCreate):
		ticker = new_stock.ticker

		if not KaseAPIClient.is_valid_ticker(ticker):
			raise HTTPException(
				status_code=404,
				detail="Ticker not found on KASE"
			)
		
		if KaseAPIClient.get_ticker_value(ticker) is None:
			raise HTTPException(
				status_code=404,
				detail="Could not get the ticker value"
			)
		
		if not await self.stock_repo.exchange_exists(new_stock.exchange_id):
			raise HTTPException(
				status_code=400,
				detail="There is no such exchange with this ID"
			)
		
		new_stock_dict = new_stock.model_dump()
		new_stock_dict["price"] = KaseAPIClient.get_ticker_value(ticker)

		if await self.stock_repo.create_one(new_stock_dict) is None:
			return {
				"status": "Failed creating the instance",
			}
		return {
			"status": "Successfully added the instance"
		}

	async def update_one_stock(self, id, field_name, new_value):
		if await self.stock_repo.update_one(id, field_name, new_value) is None:
			return {
				"status": "Failed updating the instance"
			}
		return {
			"status": "Record updated successfully", 
			"updated_id": id
		}
	
	async def delete_one_stock(self, id):
		if await self.stock_repo.delete_one(id) is None:
			return {
				"status": "Failed deleting the instance"
			}
		return {
			"status": "Record deleted successfully", 
			"updated_id": id
		}
	
	async def get_all_stocks(self):
		stocks = await self.stock_repo.get_all()

		if stocks is None:
			return {
				"status": "Failed getting the instances"
			}
		return {
			"status": "Successfully got the instances", 
			"stocks":  stocks
		}
	
	async def get_one_stock(self, id):
		instance = await self.stock_repo.get_one(id)

		if instance is None:
			return {
				"status": "Failed getting the instance"
			}
		return {
			"status": "Successfully got the instances", 
			"instance": instance
		}