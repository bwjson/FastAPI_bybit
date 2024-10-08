from src.transaction.repository import TransactionRepository
from src.transaction.service import TransactionService

def transaction_service():
	return TransactionService(TransactionRepository())