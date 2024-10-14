from fastapi import HTTPException
from src.wallet.schemas import WalletCreate
from src.wallet.repository import WalletRepository


class WalletService:
    def __init__(self, wallet_repo: WalletRepository):
        self.wallet_repo = wallet_repo

    async def create_one_wallet(self, new_wallet: WalletCreate, user):
        if await self.wallet_repo.wallet_exists(user.id):
            raise HTTPException(
                status_code=400,
                detail="your ID already has wallet",
            )

        new_wallet_dict = new_wallet.model_dump()
        new_wallet_dict["user_id"] = user.id

        if await self.wallet_repo.create_one(new_wallet_dict) is None:
            raise HTTPException(
                status_code=400,
                detail="Can not create the instance"
            )
        return {
            "status": "Successfully added the instance"
        }

    async def update_one_wallet(self, id, field_name, new_value):
        if await self.wallet_repo.update_one(id, field_name, new_value) is None:
            return {
                "status": "Failed updating the instance"
            }
        return {
            "status": "Record updated successfully",
            "updated_id": id
        }

    async def delete_one_wallet(self, id):
        if await self.wallet_repo.delete_one(id) is None:
            return {
                "status": "Failed deleting the instance"
            }
        return {
            "status": "Record deleted successfully",
            "updated_id": id
        }

    async def get_all_wallets(self):
        wallets = await self.wallet_repo.get_all()

        if wallets is None:
            return {
                "status": "Failed getting the instances"
            }
        return {
            "status": "Successfully got the instances",
            "wallets": wallets
        }

    async def get_one_wallet(self, id):
        instance = await self.wallet_repo.get_one(id)

        if instance is None:
            return {
                "status": "Failed getting the instance"
            }
        return {
            "status": "Successfully got the instances",
            "instance": instance
        }
