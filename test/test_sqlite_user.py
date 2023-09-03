# from app.infra.db.sqlite.models.user import User
# from app.infra.db.sqlite.repository import sync_session
# from app.domain.models.users import BaseUser
#

def test_sqlalchemy_pydantic_integration():
    from sqlalchemy import create_engine, String
    from sqlalchemy.orm import Session, DeclarativeBase, Mapped, mapped_column
    from typing import List, Optional

    class Base(DeclarativeBase):
        pass

    engine = create_engine("sqlite+pysqlite:///app.db", echo=True)

    class User(Base):
        __tablename__ = "user_account"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30))
        fullname: Mapped[Optional[str]]

        def __repr__(self) -> str:
            return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

    from pydantic import BaseModel


    class CreateUser(BaseModel):
        name: str
        fullname: str

        class Config:
            orm_mode = True
            from_attributes = True

    class GetUser(CreateUser):
        id: int

    Base.metadata.create_all(engine)
    sandy = CreateUser(name="sandy", fullname="Sandy Cheeks")
    session = Session(engine)
    userAdd =User(**sandy.model_dump())
    session.add(userAdd)
    session.commit()
    user = session.get(User, 1)
    getUser = GetUser.model_validate(user)
    print(getUser)