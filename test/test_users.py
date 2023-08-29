from src.models.users import BaseUser
from src.controllers.users import UserController



def test_regular_user_creation():
    user = BaseUser(
        fname="test fname",
        lname="test lname",
        tg_id=123
    )

    result = UserController.create_user(user)
    assert result == user
