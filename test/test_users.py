from src.models.users import BaseUser


def test_regular_user_creation():
    user = BaseUser(
        fname="test fname",
        lname="test lname",
        tg_id=123
    )

    assert user.fname == "test fname"
    assert user.lname == "test lname"
    assert user.tg_id == 123
