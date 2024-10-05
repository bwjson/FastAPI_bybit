from fastapi import APIRouter, Depends, HTTPException
from .utils import get_ticker_value as get_value, is_valid_ticker
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import select, insert
from .schemas import StockCreate, StockDelete, StockUpdate
from .models import *
from src.auth.models import *
from src.auth.base_config import is_authenticated
from src.auth.base_config import current_super_user


router = APIRouter(
	prefix="/api/exchange",
	tags=["exchange"]
)

@router.get("/{ticker}")
def get_ticker_value(ticker=None, user: User = Depends(is_authenticated)):
	if ticker is None:
		return HTTPException(status_code=400, detail="Ticker not provided")
	
	response = get_value(ticker)
	status = response.get("status")
	if status != "success":
		return response.get("error")
	return get_value(ticker).get("value")

@router.post("/add_stock")
async def add_stock(new_stock: StockCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_super_user)):
	if is_valid_ticker(new_stock.ticker):
		try:
			stmt = insert(Stock).values(**new_stock.dict())
			await session.execute(stmt)
			await session.commit()
			return {"status": "success"}
		except Exception as e:
			return {"status": "failed", "error": str(e)}
	else:
		return {"status": "failed", "error": "ticker not found"}

@router.put("/update_stock")
async def update_stock(updated_stock: StockUpdate, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_super_user)):
	try:
		stmt = select(Stock).filter_by(id=updated_stock.id)
		result = await session.execute(stmt)
		stock = result.scalar_one_or_none()

		if stock and is_valid_ticker(updated_stock.ticker):
			stock.id = updated_stock.id
			stock.ticker = updated_stock.ticker
			stock.exchange_id = updated_stock.exchange_id
			stock.price = updated_stock.price
			await session.commit()
			return {
				"status": "success",
				"stock_id": stock.id,
				"stock_ticker": stock.ticker, 
				"stock_exhcange_id": stock.exchange_id,
				"stock_price": stock.price
			}
		else:
			return {
				"status": "failed",
				"error": "no such stock found"
			}
	except Exception as e:
		await session.rollback()
		return {
			"status": "failed",
			"error": str(e)
		}
		

	
@router.delete("/delete_stock")
async def delete_stock(deleted_stock: StockDelete, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_super_user)):
	print(type(session))

	try:	
		stmt = select(Stock).filter_by(id=deleted_stock.id)
		result = await session.execute(stmt)
		stock = result.scalar_one_or_none()

		if stock:
			await session.delete(stock)
			await session.commit()
			return {"status": "success"}
		else:
			return {"status": "failed", "error": "stock not found"}
	except Exception as e:
		await session.rollback()
		return {"status": "failed", "error": str(e)}



		

	




