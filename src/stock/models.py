from sqlalchemy import Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

class Stock(Base):
	__tablename__ = "stock"

	id: Mapped[int] = mapped_column(primary_key=True)
	ticker: Mapped[str] = mapped_column(String(6), unique=True)
	exchange_id: Mapped[int] = mapped_column(ForeignKey("exchange.id"))
	price: Mapped[float] = mapped_column(Numeric(10, 2))





