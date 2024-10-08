from pydantic import BaseModel, field_validator, FieldValidationInfo
from src.stock.utils import is_valid_ticker


class WalletCreate(BaseModel):	
	stocks: dict

	@field_validator("stocks", mode="before")
	def set_price_from_parser(cls, value: dict, values: FieldValidationInfo):
		if not isinstance(value, dict):
			raise ValueError("Stocks must be JSON")
		
		for key, val in value.items():
			if not isinstance(key, str):
				raise ValueError(f"Invalid key '{key}': all keys must be strings")
			if not is_valid_ticker(key):
				raise ValueError(f"Ticker: {key} not found on exchanges")
			if not isinstance(val, (int, float)):
				raise ValueError(f"Invalid value for '{key}': all values must be numbers")
			
		print(value)
		return value
	
	class Config:
		from_attributes = True

	

	

			

