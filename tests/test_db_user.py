import pytest
from app.domain.models.user.dto import UserCreate, UserGet
from app.infra.db.models.user.dao import UsedDAO
import uuid

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_user_add(session, test_user: UserCreate):
    user_dao = UsedDAO()
    created_user: UserGet = await user_dao.create(session, test_user)
    assert created_user.tg_id == test_user.tg_id


@pytest.mark.asyncio
async def test_user_get_by_id(session, test_user: UserCreate):
    user_dao = UsedDAO()
    user: UserGet = await user_dao.get_by_id(session, 1)


@pytest.mark.asyncio
async def test_user_get_by_id_and_update(session, test_user_get: UserGet):
    user_dao = UsedDAO()
    user: UserGet = await user_dao.get_by_id(session, test_user_get.id)
    user.username = str(uuid.uuid4())
    updated_user: UserGet = await user_dao.update(session=session, updated_user=user)
    assert updated_user.username == user.username
