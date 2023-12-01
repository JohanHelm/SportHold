from app.domain.models.tarif.dto import TarifCreate, TarifGet
from app.infra.db.models.tarif.schema import Tarif


class TarifDAO:
    async def create(self, _session, _tarif: TarifCreate):
        sa_tarif_add: Tarif = Tarif(**_tarif.model_dump())
        async with _session() as session:
            session.add(sa_tarif_add)
            await session.commit()
        get_tarif_pydantic = TarifGet.model_validate(sa_tarif_add)
        return get_tarif_pydantic

    async def get_tarif(self, _session, rentals_amount):
        async with _session() as session:
            tarif = await session.get(Tarif, rentals_amount)
        get_tarif_pydantic = TarifGet.model_validate(tarif)
        return get_tarif_pydantic

