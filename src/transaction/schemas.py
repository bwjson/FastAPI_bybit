from pydantic import BaseModel
from src.transaction.models import TransactionType

class TransactionCreate(BaseModel):
	exchange_id: int
	stock: str
	amount: int
	price: int
	type: TransactionType