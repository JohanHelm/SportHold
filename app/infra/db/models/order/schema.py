from sqlalchemy import Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from ...models import Base


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(Integer)   # TODO реализовать завсимость от столбца с первичным ключом в таблице users
    full_name: Mapped[str] = mapped_column(String)
    tarif: Mapped[int] = mapped_column(Integer)  # TODO реализовать зависимость от таблицы с тарифами
    date_time: Mapped[DateTime] = mapped_column(DateTime)
    duration: Mapped[int] = mapped_column(Integer)
    active: Mapped[int] = mapped_column(Integer, default=1)
    prolong: Mapped[int] = mapped_column(Integer, default=1)

    def __str__(self):
        return (
            f"SQLA Order,"
            f" order_id: {self.order_id},"
            f" customer_id: {self.customer_id},"
            f" full_name: {self.full_name},"
            f" tarif: {self.tarif},"
            f" date_time: {self.date_time},"
            f" duration: {self.duration},"
            f" active: {self.active},"
            f" prolong: {self.prolong}"
        )
