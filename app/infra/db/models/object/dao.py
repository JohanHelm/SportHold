from app.domain.models.object.dto import ObjectCreate, ObjectGet
from app.infra.db.models.object.schema import Object


class ObjectDAO:
    async def create(self, _session, _object: ObjectCreate):
        sa_object_add: Object = Object(**_object.model_dump())
        async with _session() as session:
            session.add(sa_object_add)
            await session.commit()
        get_object_pydantic = ObjectGet.model_validate(sa_object_add)
        return get_object_pydantic
