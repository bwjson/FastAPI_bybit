from src.stock.repository import StockRepository
from src.stock.service import StockService

def stock_service():
	return StockService(StockRepository())