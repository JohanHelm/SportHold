from app.infra.db.sqlite.models.user import User
from app.infra.db.sqlite.repository import sync_session
from app.domain.models.users import BaseUser


def test_create_retvived_user():
    db_user = BaseUser(
        id=123,
        fullname="Leo",
        username="Vi",
        locale="ru"
    )
    sync_session.add(User(id = db_user.id, fullname = db_user.fullname, username = db_user.username, locale = db_user.locale))
    sync_session.commit()
