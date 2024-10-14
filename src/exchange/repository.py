from src.repository import SQLAlchemyRepository
from src.exchange.models import Exchange

class ExchangeRepository(SQLAlchemyRepository):
	model = Exchange