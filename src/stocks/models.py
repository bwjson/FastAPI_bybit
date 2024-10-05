from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum
from enum import Enum

from src.database import Base

class Wallet(Base):
	__tablename__ = "wallet"

	id: Mapped[int] = mapped_column(primary_key=True)
	user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
	stocks: Mapped[dict] = mapped_column(JSON, default={})
	created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
	updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

	user = relationship("User", back_populates="wallet", uselist=False)

	def get_total_amount():
		pass

class Exchange(Base):
	__tablename__ = "exchange"

	id: Mapped[int] = mapped_column(primary_key=True)
	name: Mapped[str] = mapped_column(String(30), unique=True)

class Stock(Base):
	__tablename__ = "stock"

	id: Mapped[int] = mapped_column(primary_key=True)
	ticker: Mapped[str] = mapped_column(String(6), unique=True)
	exchange_id: Mapped[int] = mapped_column(ForeignKey("exchange.id"))
	price: Mapped[str] = mapped_column(String(10))

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Transaction(Base):
	__tablename__ = "transaction"

	id: Mapped[int] = mapped_column(primary_key=True)
	wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"))
	exchange_id: Mapped[int] = mapped_column(ForeignKey("exchange.id"))
	type: Mapped[TransactionType] = mapped_column(SqlEnum(TransactionType))




