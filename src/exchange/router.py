from typing import Annotated
from fastapi import APIRouter, Depends
from src.exchange.service import ExchangeService
from .schemas import ExchangeCreate, ExchangeDelete
from .models import *
from src.auth.models import *
from src.auth.base_config import current_super_user, is_authenticated
from src.exchange.dependencies import exchange_service


router = APIRouter(
	prefix="/api/exchange",
	tags=["exchange"]
)

@router.post("/add_exchange")
async def add_stock(new_exchange: ExchangeCreate, stock_service: Annotated[ExchangeService, Depends(exchange_service)], user: User = Depends(current_super_user)):
	return await stock_service.create_one_stock(new_exchange)


@router.delete("/delete_exchange")
async def delete_stock(deleted_exchange: ExchangeDelete, stock_service: Annotated[ExchangeService, Depends(exchange_service)], user: User = Depends(current_super_user)):
	return await stock_service.delete_one_stock(deleted_exchange.id)



		

	




