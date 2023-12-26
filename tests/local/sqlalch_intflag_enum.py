from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, mapped_column, relationship
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Integer, String

from sqlalchemy.orm.base import Mapped

class RentalTypes(Enum):
    REGULAR = 0

    def custom_print(self):
        return self.name

if TYPE_CHECKING:
    from app.infra.db.models.schedule.schema import Schedule
    from app.infra.db.models.slot.schema import Slot
    from app.infra.db.models.record.schema import Record

Base: DeclarativeBase = declarative_base()


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    type: Mapped[int] = mapped_column(Integer, default=RentalTypes.REGULAR)

    # schedules: Mapped[List["Schedule"]] = relationship()
    # slots: Mapped[List["Slot"]] = relationship()
    # records: Mapped[List["Record"]] = relationship()

    def __str__(self):
        return (
            f"SQLA Rental, "
            f"id: {self.id}, "
            f"category: {RentalTypes(self.type).custom_print()}, "
            f"name: {self.name}, "
            f"description: {self.type} "
            # f"schedules: {len(self.schedules)} "
            # f"slots: {len(self.slots)} "
            # f"records: {len(self.records)}"
        )


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def main():
    db: Session = SessionLocal()

    rental: Rental = Rental(
        name="test",
        description = "test",
        type = RentalTypes.REGULAR,
    )

    print(rental)


if __name__ == "__main__":
    main()
