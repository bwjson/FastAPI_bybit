from src.repository import SQLAlchemyRepository
from src.wallet.models import Wallet

class TransactionRepository(SQLAlchemyRepository):
	model = Wallet