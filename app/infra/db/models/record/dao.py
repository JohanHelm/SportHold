from app.domain.models.record.dto import RecordCreate, RecordGet
from app.infra.db.models.record.schema import Record


class RecordDAO:
    async def create(self, _session, _record: RecordCreate):
        sa_record_add: Record = Record(**_record.model_dump())
        async with _session() as session:
            session.add(sa_record_add)
            await session.commit()
        get_record_pydantic = RecordGet.model_validate(sa_record_add)
        return get_record_pydantic
