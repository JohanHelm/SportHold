from sqlalchemy import String
from sqlalchemy.orm import Mapped, declarative_base
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class Object(Base):
    __tablename__ = "object"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    desc: Mapped[str] = mapped_column(String)
