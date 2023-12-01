from sqlalchemy import Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ...models import Base


class Promo(Base):
    __tablename__ = "promos"

    promo_code: Mapped[str] = mapped_column(primary_key=True)
    active: Mapped[int] = mapped_column(Integer, default=1)
    promo_money: Mapped[int] = mapped_column(Integer)
    used_times: Mapped[int] = mapped_column(Integer, default=0)
    expires_at: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    times_to_use: Mapped[int] = mapped_column(Integer, nullable=True)

    def __str__(self):
        return (
            f"SQLA Promo,"
            f" promo_code: {self.promo_code},"
            f" active: {self.active},"
            f" promo_money: {self.promo_money},"
            f" used_times: {self.used_times},"
            f" expires_at: {self.expires_at},"
            f" times_to_use: {self.times_to_use}"
        )
