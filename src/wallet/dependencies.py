from src.wallet.repository import WalletRepository
from src.wallet.service import WalletService

def wallet_service():
    return WalletService(WalletRepository())