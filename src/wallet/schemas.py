from pydantic import BaseModel
from typing import Union


class WalletCreate(BaseModel):
	stocks: dict
			
class WalletDelete(BaseModel):
	id: int
    
class WalletUpdate(BaseModel):
	id: int
	field: str
	new_value: Union[int, float, dict]
	
	

	

	

			

