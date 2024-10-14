from src.exchange.repository import ExchangeRepository
from src.exchange.service import ExchangeService

def exchange_service():
	return ExchangeService(ExchangeRepository())