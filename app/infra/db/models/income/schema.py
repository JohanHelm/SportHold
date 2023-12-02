from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ...models import Base

from app.domain.models.income.dto import PaymentMethod


class Income(Base):
    __tablename__ = "incomes"

    customer_id: int
    full_name: Mapped[str] = mapped_column(String)
    summ: Mapped[int] = mapped_column(Integer)
    date_time: Mapped[DateTime] = mapped_column(DateTime)
    method: Mapped[int] = mapped_column(Integer)

    def __str__(self):
        return (
            f"SQLA Income,"
            f" customer_id: {self.customer_id},"
            f" full_name: {self.full_name},"
            f" summ: {self.summ},"
            f" date_time: {self.date_time},"
            f" method: {PaymentMethod(self.method)}"
        )
