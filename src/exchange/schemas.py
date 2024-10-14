from pydantic import BaseModel
from typing import Union

class ExchangeCreate(BaseModel):
	id: int
	name: str
			
class ExchangeDelete(BaseModel):
	id: int
    

