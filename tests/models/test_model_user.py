from datetime import datetime
import pytest
from app.domain.models.user.dto import SubscrptionType, UserBase, UserRole

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_user_model(user_create_model: UserBase):
    
    assert user_create_model.roles == UserRole.REGULAR
    


