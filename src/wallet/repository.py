from src.repository import SQLAlchemyRepository
from src.wallet.models import Wallet

class WalletRepository(SQLAlchemyRepository):
	model = Wallet