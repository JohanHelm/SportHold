from src.models.users import BaseUser
from src.controllers.users import UserController
from src.controllers.memorydb import InMemoryDB

db = InMemoryDB
user_control = UserController(db)

def test_create_retvive_user():
    user = BaseUser(
        fname="test fname",
        lname="test lname",
        tg_id=123
    )

    result_user: BaseUser = user_control.save_user(user)
    assert result_user == user_control.get_user_by_tg_id(user.tg_id)
