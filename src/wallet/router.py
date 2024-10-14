from typing import Annotated
from fastapi import APIRouter, Depends
from src.wallet.service import WalletService
from .schemas import WalletCreate, WalletDelete, WalletUpdate
from .models import *
from src.auth.models import *
from src.auth.base_config import current_super_user, is_authenticated
from src.wallet.dependencies import wallet_service
from fastapi_cache.decorator import cache

router = APIRouter(
	prefix='/api/wallet',
	tags=["wallet"]
)


@router.post("/add_wallet")
async def add_wallet(new_wallet: WalletCreate, wallet_service: Annotated[WalletService, Depends(wallet_service)], user: User = Depends(current_super_user)):
	return await wallet_service.create_one_wallet(new_wallet, user)

@router.get("/get_all")
@cache(expire=60)
async def get_all_wallets(wallet_service: Annotated[WalletService, Depends(wallet_service)], user: User = Depends(is_authenticated)):
	return await wallet_service.get_all_wallets()

@router.get("/get_one/{wallet_id}")
@cache(expire=60)
async def get_wallet(wallet_id: int, wallet_service: Annotated[WalletService, Depends(wallet_service)], user: User = Depends(is_authenticated)):
	return await wallet_service.get_one_wallet(wallet_id)


@router.patch("/update_wallet")
async def update_stock(updated_wallet: WalletUpdate, wallet_service: Annotated[WalletService, Depends(wallet_service)], user: User = Depends(current_super_user)):
	return await wallet_service.update_one_wallet(updated_wallet.id, updated_wallet.field, updated_wallet.new_value)


@router.delete("/delete_wallet")
async def delete_stock(deleted_wallet: WalletDelete, wallet_service: Annotated[WalletService, Depends(wallet_service)], user: User = Depends(current_super_user)):
	return await wallet_service.delete_one_wallet(deleted_wallet.id)

