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
	stocks: Mapped[dict] = mapped_column(JSON, default={}, nullable=True)
	created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now())
	updated_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

	user = relationship("User", back_populates="wallet", uselist=False)
	

	def get_total_amount():
		pass