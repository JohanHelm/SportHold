from app.domain.models.object.dto import ObjectCreate, ObjectGet
from app.infra.db.models.object.schema import Object


class ObjectDAO:
    def __init__(self, session):
        self.session = session

    async def create(self, _object: ObjectCreate):
        sa_object_add: Object = Object(**_object.model_dump())
        async with self.session() as session:
            session.add(sa_object_add)
            await session.commit()
            get_object_pydantic = ObjectGet.model_validate(sa_object_add)
            print(get_object_pydantic)
            return get_object_pydantic
