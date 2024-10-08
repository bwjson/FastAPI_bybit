from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from sqlalchemy import select, insert
from .schemas import WalletCreate
from .models import *
from src.auth.models import *
from src.auth.base_config import current_super_user, is_authenticated

router = APIRouter(
	prefix='/api/wallet',
	tags=["wallet"]
)

# для простых пользователей можно создавать только на их же id
@router.post("/add_wallet")
async def wallet_create(new_wallet: WalletCreate, session: AsyncSession = Depends(get_async_session), user: User = Depends(is_authenticated)):
	query = select(Wallet).filter_by(user_id=user.id)
	has_wallet_data = await session.execute(query)
	has_wallet = has_wallet_data.scalars().all()

	if has_wallet:
		return {
			"status": "failed",
			"error": "your ID already has wallet",
		}
	
	try:
		stmt = insert(Wallet).values(user_id=user.id, stocks=new_wallet.stocks)
		await session.execute(stmt)
		await session.commit()
		return {
			"status": "success"
		}
	except Exception as e:
		return {
			"status": "failed",
			"error": str(e)
		}

