from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean, MetaData
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum as SqlEnum
from enum import Enum

from src.database import Base

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





