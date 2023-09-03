from app.domain.models.user.dto import UserCreate, UserGet
from app.infra.db.sqlite.repository import Base


#

def test_sqlalchemy_pydantic_integration():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    from app.infra.db.sqlite.models.user import User
    engine = create_engine("sqlite+pysqlite:///app.db", echo=True)
    Base.metadata.create_all(engine)
    sandy = UserCreate(
        tg_id=123,
        first_name="anton",
        last_name="bezkrovny",
        username="@antonbezkrovnyy",
        language_code="ru",
        is_premium=True,
        is_bot=False
    )
    session = Session(engine)
    user_add = User(**sandy.model_dump())
    session.add(user_add)
    session.commit()
    user = session.get(User, 1)
    get_user = UserGet.model_validate(user)
    print(get_user)
