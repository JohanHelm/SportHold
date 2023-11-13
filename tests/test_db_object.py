import pytest
from app.domain.models.object.dto import ObjectGet, ObjectCreate
from app.infra.db.models.object.dao import ObjectDAO

pytest_plugins = ("pytest_asyncio",)


@pytest.mark.asyncio
async def test_object_add(session, test_object: ObjectCreate):
    object_dao = ObjectDAO()
    created_object: ObjectGet = await object_dao.create(session, test_object)
    assert created_object.name == test_object.name