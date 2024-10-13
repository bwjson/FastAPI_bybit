from pydantic import BaseModel
from typing import Union

class StockCreate(BaseModel):
	ticker: str
	exchange_id: int
			
class StockDelete(BaseModel):
	id: int
    
class StockUpdate(BaseModel):
	id: int
	field: str
	new_value: Union[str, int, float]

