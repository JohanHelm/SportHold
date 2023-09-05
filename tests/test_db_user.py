import pytest
from app.domain.models.user.dto import UserCreate, UserGet
from app.infra.db.models.user.dao import UsedDAO

pytest_plugins = ('pytest_asyncio',)

PK_ID = None


@pytest.mark.asyncio
async def test_user_add(async_db_session):
    session = await async_db_session
    user_dao = UsedDAO(session)
    test_user_pydantic = UserCreate(
        tg_id=123,
        first_name="anton",
        last_name="bezkrovny",
        username="@antonbezkrovnyy",
        language_code="ru",
        is_premium=True,
        is_bot=False
    )
    created_user: UserGet = await user_dao.create(test_user_pydantic)
    pytest.test_user_id = created_user.id
    assert created_user.tg_id == test_user_pydantic.tg_id


@pytest.mark.asyncio
async def test_user_get_by_id(async_db_session):
    session = await async_db_session
    user_dao = UsedDAO(session)
    user = await user_dao.get_by_id(id=pytest.test_user_id)
    assert user.id == pytest.test_user_id


@pytest.mark.asyncio
async def test_user_get_by_id_and_update(async_db_session):
    session = await async_db_session
    user_dao = UsedDAO(session)
    user = await user_dao.get_by_id(id=pytest.test_user_id)
    user.username = "changeme"
    updated_user = await user_dao.update(user)
    assert updated_user.username == "changeme"