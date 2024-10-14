from fastapi import HTTPException
from src.transaction.schemas import TransactionCreate, WalletTransactionCreate
from src.transaction.repository import TransactionRepository
from src.transaction.tasks import send_email_order_report


class TransactionService:
    def __init__(self, trans_repo: TransactionRepository):
        self.trans_repo = trans_repo

    async def validate_transaction(self, new_transaction: TransactionCreate, user):
        if not await self.trans_repo.wallet_exists(user.id):
            raise HTTPException(
                status_code=400,
                detail="You should create wallet first"
            )

        if not await self.trans_repo.exchange_exists(new_transaction.exchange_id):
            raise HTTPException(
                status_code=400,
                detail="There is no such exchange with this ID"
            )

        if not await self.trans_repo.ticker_exists(new_transaction.stock):
            raise HTTPException(
                status_code=400,
                detail="There is no such ticker"
            )

    async def validate_sell_transaction(self, new_transaction: TransactionCreate, user, wallet_id):
        stocks = await self.trans_repo.get_wallet_stocks(user.id)
        blocked_stocks = await self.trans_repo.get_blocked_stocks(wallet_id, new_transaction.stock, new_transaction.exchange_id)
        current_stocks = stocks[new_transaction.stock]

        try:
            if stocks[new_transaction.stock] < new_transaction.amount:
                raise HTTPException(
                    status_code=400,
                    detail="You don't have needed amount of this ticker in your wallet"
                )
            if blocked_stocks + new_transaction.amount > current_stocks:
                raise HTTPException(
                    status_code=400,
                    detail=f"You have blocked stocks for other transactions: {blocked_stocks}; " \
                            f"Your available balance: {current_stocks - blocked_stocks}"
                )
        except KeyError:
            raise HTTPException(
                status_code=400,
                detail="You don't have this ticker in your wallet"
            )

    async def validate_buy_transaction(self, new_transaction: TransactionCreate, user, wallet_id):
        user_balance = await self.trans_repo.get_user_balance(user.id)
        blocked_funds = await self.trans_repo.get_blocked_funds(wallet_id, new_transaction.exchange_id)
        if user_balance is None or user_balance < new_transaction.amount * new_transaction.price:
            raise HTTPException(
                status_code=400,
                detail="Your balance is lower than cost of transaction"
            )
        if blocked_funds + new_transaction.amount * new_transaction.price > user_balance:
            raise HTTPException(
                status_code=400,
                detail=f"You have blocked balance for other transactions: {blocked_funds}; " \
                        f"Your available balance: {user_balance - blocked_funds}"
            )

    async def create_transaction(self, new_transaction: TransactionCreate, user):
        wallet_id = await self.trans_repo.get_wallet_id(user.id)

        await self.validate_transaction(new_transaction, user)

        if new_transaction.type == "SELL":
            await self.validate_sell_transaction(new_transaction, user, wallet_id)
        elif new_transaction.type == "BUY":
            await self.validate_buy_transaction(new_transaction, user, wallet_id)

        transaction_dict = new_transaction.model_dump()
        transaction_dict["wallet_id"] = wallet_id

        await self.trans_repo.create_one(transaction_dict)
        return {
            "status": "success",
            "new_transaction": new_transaction
        }

    async def validate_wallet_transaction(self, new_transaction: WalletTransactionCreate, user):
        if not await self.trans_repo.wallet_exists(user.id):
            raise HTTPException(
                status_code=400,
                detail="You should create wallet first"
            )

        if not await self.trans_repo.exchange_exists(new_transaction.exchange_id):
            raise HTTPException(
                status_code=400,
                detail="There is no such exchange with this ID"
            )

    async def execute_topup_transaction(self, new_transaction: WalletTransactionCreate, user, wallet_id):
        current_balance = await self.trans_repo.get_user_balance(user.id)
        withdrawal_amount = new_transaction.deposit
        new_balance = current_balance + withdrawal_amount
        await self.trans_repo.change_wallet_balance(wallet_id, new_balance)

    async def execute_withdraw_transaction(self, new_transaction: WalletTransactionCreate, user, wallet_id):
        current_balance = await self.trans_repo.get_user_balance(user.id)
        withdrawal_amount = new_transaction.deposit

        if withdrawal_amount > current_balance:
            raise HTTPException(
                status_code=400,
                detail=f"You are missing {withdrawal_amount - current_balance}, can not execute transaction"
            )

        new_balance = current_balance - withdrawal_amount
        await self.trans_repo.change_wallet_balance(wallet_id, new_balance)

    async def create_wallet_transaction(self, new_transaction: WalletTransactionCreate, user):
        wallet_id = await self.trans_repo.get_wallet_id(user.id)

        self.validate_wallet_transaction(new_transaction, user)

        if new_transaction.type == "TOPUP":
            self.validate_topup_transaction(new_transaction, user, wallet_id)
        elif new_transaction.type == "WITHDRAW":
            self.validate_withdraw_transaction(new_transaction, user, wallet_id)


        transaction_dict = new_transaction.model_dump()
        transaction_dict["wallet_id"] = wallet_id
        await self.trans_repo.create_one_wallet_transaction(transaction_dict)
        return {
            "status": "success",
            "new_transaction": new_transaction
        }

    async def check_transaction_match(self):
        sell_orders = await self.trans_repo.get_sell_orders()
        buy_orders = await self.trans_repo.get_buy_orders()

        for sell_order in sell_orders:
            for buy_order in buy_orders:
                if not sell_order.price <= buy_order.price:
                    continue
                if not sell_order.stock == buy_order.stock:
                    continue
                if not sell_order.exchange_id == buy_order.exchange_id:
                    continue
                if not sell_order.wallet_id != buy_order.wallet_id:
                    continue
                await self.execute_order(sell_order, buy_order)
                return

    async def execute_order(self, buy_transaction, sell_transaction):
        order_price = min(buy_transaction.price, sell_transaction.price)
        order_amount = min(buy_transaction.amount, sell_transaction.amount)

        await self.trans_repo.change_user_balance(buy_transaction.wallet_id, order_amount, order_price, buy_transaction.type)
        await self.trans_repo.change_user_balance(sell_transaction.wallet_id, order_amount, order_price, sell_transaction.type)

        await self.trans_repo.change_user_stocks(buy_transaction.wallet_id, buy_transaction.stock, order_amount, buy_transaction.type)
        await self.trans_repo.change_user_stocks(sell_transaction.wallet_id, sell_transaction.stock, order_amount, sell_transaction.type)

        await self.trans_repo.delete_one(buy_transaction.id)
        await self.trans_repo.delete_one(sell_transaction.id)

        send_email_order_report.delay(buy_transaction.id, buy_transaction.wallet_id, buy_transaction.stock, buy_transaction.amount, buy_transaction.type)
        send_email_order_report.delay(sell_transaction.id, sell_transaction.wallet_id, sell_transaction.stock, sell_transaction.amount, sell_transaction.type)

