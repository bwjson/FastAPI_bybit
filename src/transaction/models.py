from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum
from enum import Enum

from src.database import Base

class TransactionType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Transaction(Base):
	__tablename__ = "transaction"

	id: Mapped[int] = mapped_column(primary_key=True)
	wallet_id: Mapped[int] = mapped_column(ForeignKey("wallet.id"))
	exchange_id: Mapped[int] = mapped_column(ForeignKey("exchange.id"))
	stock: Mapped[str] = mapped_column(String(10), nullable=False)
	amount: Mapped[int] = mapped_column(Integer, nullable=False)
	type: Mapped[TransactionType] = mapped_column(SqlEnum(TransactionType, name="transactiontype", create_type=False))
      
	extend_existing = True