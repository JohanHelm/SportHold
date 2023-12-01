from app.domain.models.promo.dto import PromoCreate, PromoGet
from app.infra.db.models.promo.schema import Promo


class PromoDAO:
    async def create(self, _session, _promo: PromoCreate):
        sa_promo_add: Promo = Promo(**_promo.model_dump())
        async with _session() as session:
            session.add(sa_promo_add)
            await session.commit()
        get_promo_pydantic = PromoGet.model_validate(sa_promo_add)
        return get_promo_pydantic


