import pytest
from app.domain.models.rental.dto import RentalBase, RentalType
from app.domain.models.user.dto import UserBase


@pytest.fixture(scope="session")
def user_model():
    user_model = UserBase(
        id=123,
        username="avasilii",
        fullname="Vasilii Anisimov",
    )
    return user_model


@pytest.fixture(scope="session")
def rental_model():
    rental_model = RentalBase(
        name="Ping-pong table",
        description="Ping-pong table on 2nd floor BC",
        rental_type=RentalType.REGULAR,
    )
    return rental_model
