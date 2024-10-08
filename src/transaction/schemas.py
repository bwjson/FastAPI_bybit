from pydantic import BaseModel
from src.transaction.models import TransactionType

class TransactionCreate(BaseModel):
	wallet_id: int
	exchange_id: int
	stock: str
	amount: int
	type: TransactionType