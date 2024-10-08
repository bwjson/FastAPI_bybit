from src.repository import SQLAlchemyRepository
from src.stock.models import Stock

class StockRepository(SQLAlchemyRepository):
	model = Stock