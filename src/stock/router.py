from typing import Annotated
from fastapi import APIRouter, Depends
from src.stock.service import StockService
from .schemas import StockCreate, StockDelete, StockUpdate
from .models import *
from src.auth.models import *
from src.auth.base_config import current_super_user, is_authenticated
from src.stock.dependencies import stock_service


router = APIRouter(
	prefix="/api/stock",
	tags=["stock"]
)

@router.post("/add_stock")
async def add_stock(new_stock: StockCreate, stock_service: Annotated[StockService, Depends(stock_service)], user: User = Depends(current_super_user)):
	return await stock_service.create_one_stock(new_stock)

@router.get("/get_all")
async def delete_stock(stock_service: Annotated[StockService, Depends(stock_service)], user: User = Depends(is_authenticated)):
	return await stock_service.get_all_stocks()

@router.get("/get_one/{stock_id}")
async def delete_stock(stock_id: int,stock_service: Annotated[StockService, Depends(stock_service)], user: User = Depends(is_authenticated)):
	return await stock_service.get_one_stock(stock_id)


@router.patch("/update_stock")
async def update_stock(updated_stock: StockUpdate, stock_service: Annotated[StockService, Depends(stock_service)], user: User = Depends(current_super_user)):
	return await stock_service.update_one_stock(updated_stock.id, updated_stock.field, updated_stock.new_value)


@router.delete("/delete_stock")
async def delete_stock(deleted_stock: StockDelete, stock_service: Annotated[StockService, Depends(stock_service)], user: User = Depends(current_super_user)):
	return await stock_service.delete_one_stock(deleted_stock.id)





		

	




