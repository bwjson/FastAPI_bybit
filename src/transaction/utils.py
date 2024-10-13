import asyncio
from src.transaction.dependencies import transaction_service

async def check_match():
    while True:
        service = transaction_service()
        await service.check_transaction_match()
        await asyncio.sleep(20)