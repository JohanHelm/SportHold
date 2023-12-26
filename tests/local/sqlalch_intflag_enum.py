from datetime import datetime
from enum import IntFlag as IF, IntEnum as EN

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Integer, String, DateTime

from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class UserRole(IF):
    REGULAR = 1
    PARTNER = 2
    ADMIN = 4
    MANAGER = 8
    EMPLOYEE = 16
    OWNER = 32
    WORKER = 64
    PAID = 128

    def custom_print(self):
        return "|".join(val.name for val in UserRole if self.value & val)


class UserStatus(EN):
    INACTIVE = 0
    ACTIVE = 1

    def custom_print(self):
        return self.name


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    username: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now())
    status: Mapped[int] = mapped_column(Integer, default=UserStatus.ACTIVE)
    roles: Mapped[int] = mapped_column(Integer, default=UserRole.REGULAR)

    def __str__(self):
        return (
            f"SQLA User, "
            f"id: {self.id}, "
            f"username: {self.username}, "
            f"fullname: {self.fullname}, "
            f"created_at: {self.created_at}, "
            f"status: {UserStatus(self.status).custom_print()}, "
            f"roles: {UserRole(self.roles).custom_print()}"
        )


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def main():
    db: Session = SessionLocal()

    user = User(
        username="Test",
        fullname="test user",
        status=UserStatus.ACTIVE,
        roles=UserRole.ADMIN | UserRole.EMPLOYEE,
    )

    db.add(user)
    db.commit()

    print(user)
    print(f"UserRole.MANAGER in user.roles: {UserRole.MANAGER in UserRole(user.roles)}")
    print(f"UserStatus.ACTIVE == user.status :{UserStatus.ACTIVE == user.status}")


if __name__ == "__main__":
    main()
