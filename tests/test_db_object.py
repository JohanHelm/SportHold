import pytest
from app.domain.models.object.dto import ObjectGet, ObjectCreate
from app.infra.db.models.object.dao import ObjectDAO

pytest_plugins = ('pytest_asyncio',)

@pytest.mark.asyncio
async def test_object_add(async_db_session):
    session = await async_db_session
    object_dao = ObjectDAO(session)
    test_object_pydantic = ObjectCreate(
        name="pp table",
        desc="on 2nd floor"
    )
    created_object: ObjectGet = await object_dao.create(test_object_pydantic)
    pytest.test_object_id = created_object.id
    assert created_object.name == test_object_pydantic.name

#
# @pytest.mark.asyncio
# async def test_user_get_by_id(async_db_session):
#     session = await async_db_session
#     user_dao = UsedDAO(session)
#     user = await user_dao.get_by_id(id=pytest.test_user_id)
#     assert user.id == pytest.test_user_id
#
#
# @pytest.mark.asyncio
# async def test_user_get_by_id_and_update(async_db_session):
#     session = await async_db_session
#     user_dao = UsedDAO(session)
#     user = await user_dao.get_by_id(id=pytest.test_user_id)
#     user.username = "changeme"
#     updated_user = await user_dao.update(user)
#     assert updated_user.username == "changeme"