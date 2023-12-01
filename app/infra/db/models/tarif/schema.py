from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from ...models import Base


class Tarif(Base):
    __tablename__ = "tarifs"

    rentals_amount: Mapped[int] = mapped_column(primary_key=True)
    one_month: Mapped[int] = mapped_column(Integer)
    three_month: Mapped[int] = mapped_column(Integer)
    six_month: Mapped[int] = mapped_column(Integer)
    one_year: Mapped[int] = mapped_column(Integer)
    two_years: Mapped[int] = mapped_column(Integer)
    three_years: Mapped[int] = mapped_column(Integer)

    def __str__(self):
        return (
            f"SQLA Tarif,"
            f" tarif: {self.rentals_amount},"
            f" one_month: {self.one_month},"
            f" six_month: {self.six_month},"
            f" one_year: {self.one_year},"
            f" two_years: {self.two_years},"
            f" three_years: {self.three_years}"
        )
