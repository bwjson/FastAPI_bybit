from pydantic import BaseModel
from src.transaction.models import TransactionType, WalletTransactionType

class TransactionCreate(BaseModel):
    exchange_id: int
    stock: str
    amount: int
    price: int
    type: TransactionType

class WalletTransactionCreate(BaseModel):
    exchange_id: int
    deposit: int
    type: WalletTransactionType

