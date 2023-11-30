from datetime import datetime
import pytest
from app.domain.models.user.dto import SubscrptionType, UserBase, UserCreate, UserRole

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_user_model(user_create_model: UserCreate):
    assert user_create_model.wallet_balance == 0
    assert user_create_model.roles == UserRole.REGULAR
    assert user_create_model.subscription_type == SubscrptionType.REGULAR
    assert user_create_model.subscription_valid_for >= datetime.today().date()


