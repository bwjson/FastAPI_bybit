from pydantic import BaseModel, field_validator, FieldValidationInfo
from src.stocks.utils import get_ticker_value, is_valid_ticker as is_valid


class StockCreate(BaseModel):
	id: int
	ticker: str
	exchange_id: int
	price: str = None

	@field_validator("price", mode="before")
	def set_price_from_parser(cls, value, values: FieldValidationInfo):
		ticker = values.data.get("ticker")
		print(ticker)
		if ticker:
			try:
				response = get_ticker_value(ticker)
				if response.get("status") == "success":
					return response.get("value")
			except Exception as e:
				return "N/A"
			
class StockDelete(BaseModel):
	id: int
	ticker: str
	exchange_id: int
    
class StockUpdate(BaseModel):
	id: int
	ticker: str
	exchange_id: int
	price: str

