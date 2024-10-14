from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.auth.schemas import UserCreate, UserRead
from src.auth.base_config import auth_backend, fastapi_users
from src.stock.router import router as stock_router
from src.wallet.router import router as wallet_router
from src.exchange.router import router as exchange_router
from src.transaction.router import router as transaction_router

app = FastAPI()

app.include_router(stock_router)
app.include_router(wallet_router)
app.include_router(transaction_router)
app.include_router(exchange_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)