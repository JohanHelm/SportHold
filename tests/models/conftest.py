from datetime import date, timedelta
import pytest

from app.domain.models.user.dto import UserCreate, UserRole, SubscrptionType


@pytest.fixture(scope="session")
def user_create_model():
    user_create_model = UserCreate(
        tg_id=123,
        username="Vasilii Anisimov",
        roles=UserRole.REGULAR,
        subscription_type=SubscrptionType.REGULAR,
        subscription_valid_for=date.today() + timedelta(days=30),
        wallet_balance=0,
    )
    return user_create_model
